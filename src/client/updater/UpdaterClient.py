"""
UpdaterClient 模块
==================
程序更新客户端，负责检查更新、判定增量/全量、下载更新包并执行更新。

包含：
  - 检查新版本（check_new_version）
  - 判定更新方式（decide_update）
  - 自动下载更新（__auto_update）
  - 生成更新脚本（__run_update_script）
"""
import logging
import os
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
import zipfile
from typing import Tuple

from PySide6.QtWidgets import QMessageBox
from packaging import version

from src.client import RequestClient
from src.client.updater.GithubHostsProxy import GithubHostsProxy
from src.config import Config
from src.config.GlobalConfig import GlobalConstants
from src.utils import BoxPop
from src.utils.ThreadPoolManager import get_thread_pool


class _UpdateCancelled(Exception):
    """用户取消更新时抛出的内部异常"""
    pass


def build_path(path: str):
    """获取打包后或开发环境下的绝对路径"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        p = os.path.dirname(sys.executable)
        return rf'{p}\{path}'
    # 如果是在开发环境中运行
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    return rf'{p}\{path}'


class UpdaterClient:
    """程序更新客户端"""

    @staticmethod
    def check_new_version(win, quiet: bool = True):
        """检查新版本，若有更新则弹出提示"""
        # 如果是安静模式,且无勾选检查更新
        if quiet and not Config.app_check_update():
            return

        # 检查更新
        def __check_update_result(window, result, e):
            if not result:
                result = (False, '未知错误', None)
            status_flag, message, update_info = result
            if e:
                logging.error(f"检查版本更新出现错误：\n {str(e)}")
                status_flag = False
                message = "无法获取版本信息"
            if status_flag:
                buttons = {
                    "立即更新": QMessageBox.ButtonRole.AcceptRole,
                    "前往发布页": QMessageBox.ButtonRole.ActionRole,
                    "取消": QMessageBox.ButtonRole.RejectRole
                }
                if quiet:
                    buttons = {
                        "立即更新": QMessageBox.ButtonRole.AcceptRole,
                        "前往发布页": QMessageBox.ButtonRole.ActionRole,
                        "不再提醒": QMessageBox.ButtonRole.DestructiveRole,
                        "取消": QMessageBox.ButtonRole.RejectRole
                    }
                click_result = BoxPop.custom_question(window, message, buttons)

                if click_result == QMessageBox.ButtonRole.AcceptRole:
                    # 自动下载更新
                    UpdaterClient.__auto_update(window, update_info)
                elif click_result == QMessageBox.ButtonRole.ActionRole:
                    webbrowser.open(f"{GlobalConstants.GITHUB_URL}/releases")
                if quiet and click_result == QMessageBox.ButtonRole.DestructiveRole:
                    Config.app_check_update(False)
            elif not quiet:
                BoxPop.info(window, message)

        get_thread_pool().submit_task(UpdaterClient.__check_version, __check_update_result, win, not quiet)

    @staticmethod
    def __check_version() -> Tuple[bool, str, dict]:
        # bool = 是否有更新
        # str = 更新内容,错误消息
        # dict = 更新信息（version / dependency_version / incremental_url / full_url）
        msg = '无法获取版本信息'
        update_info = None
        response = RequestClient.get_instance().get(f"{GlobalConstants.GITHUB_API_URL}/releases/latest")
        response.raise_for_status()
        data = response.json()
        latest_version = data.get('tag_name')
        if latest_version is None:
            return False, msg, update_info
        if version.parse(GlobalConstants.APP_VERSION) >= version.parse(latest_version):
            return False, '当前是最新版本', update_info
        else:
            body = data.get('body')
            # 收集 Release assets 的下载地址
            assets = {asset.get('name'): asset.get('browser_download_url', '')
                      for asset in data.get('assets', [])}
            full_url = assets.get('QsBeanfun.zip', '')
            incremental_url = assets.get('Beanfun.exe', '')

            # 解析 update.json（若存在），获取依赖库基线版本
            dependency_version = latest_version
            update_json_url = assets.get('update.json', '')
            if update_json_url:
                try:
                    resp = RequestClient.get_instance().get(update_json_url, timeout=30)
                    if resp.status_code == 200:
                        update_data = resp.json()
                        dependency_version = update_data.get('dependency_version', latest_version)
                        incremental_url = update_data.get('incremental_url', incremental_url)
                        full_url = update_data.get('full_url', full_url)
                except Exception as e:
                    logging.warning(f"解析 update.json 失败，回退默认值: {str(e)}")

            update_info = {
                'version': latest_version,
                'dependency_version': dependency_version,
                'incremental_url': incremental_url,
                'full_url': full_url,
            }
            msg = f'发现新版本：{latest_version}\n{body}\n是否立即更新?'
            return True, msg, update_info

    @staticmethod
    def decide_update(current_version: str, update_info: dict) -> Tuple[str, str]:
        """根据用户当前版本与依赖库基线版本，决定更新方式。

        默认增量更新：只有当用户当前版本落后于依赖库基线版本时才全量更新。

        Returns:
            (update_type, download_url): update_type 为 'incremental' 或 'full'
        """
        if not update_info:
            return 'full', ''
        dependency_version = update_info.get('dependency_version', update_info.get('version', ''))
        try:
            # 用户当前版本落后于依赖库基线 → 本地依赖库过旧，必须全量
            if version.parse(current_version) < version.parse(dependency_version):
                return 'full', update_info.get('full_url', '')
        except Exception as e:
            logging.warning(f"版本比较失败，回退全量更新: {str(e)}")
            return 'full', update_info.get('full_url', '')
        # 默认增量更新：只下载 Beanfun.exe
        return 'incremental', update_info.get('incremental_url', '')

    @staticmethod
    def __auto_update(window, update_info: dict):
        """自动下载并更新程序（支持增量/全量）"""
        if not update_info:
            BoxPop.warn(window, "未找到更新包下载地址，请前往 GitHub 手动下载")
            webbrowser.open(f"{GlobalConstants.GITHUB_URL}/releases")
            return

        # 判定更新方式：默认增量，仅当用户版本落后于依赖库基线时全量
        update_type, download_url = UpdaterClient.decide_update(GlobalConstants.APP_VERSION, update_info)
        if not download_url:
            BoxPop.warn(window, "未找到更新包下载地址，请前往 GitHub 手动下载")
            webbrowser.open(f"{GlobalConstants.GITHUB_URL}/releases")
            return

        # 延迟导入，避免与 WinManager -> MenuManager -> Config -> BaseTools 形成循环导入
        from src.window.DownloadWin import DownloadWin

        # 创建独立的下载进度窗口，给用户美观的下载反馈
        download_win = DownloadWin(window)
        download_win.show()

        # 取消标志：用户关闭窗口时置位，后台任务据此停止
        cancel_event = threading.Event()
        # 代理实例（供更新完成后停止）
        proxy = None

        def __on_cancel():
            cancel_event.set()

        download_win.cancel_requested.connect(__on_cancel)

        # 在后台线程执行下载更新，通过回调在主线程处理错误提示
        def __do_update():
            nonlocal proxy
            try:
                # 0. 若用户已关闭窗口，直接取消
                if cancel_event.is_set():
                    raise _UpdateCancelled()

                # 1. 启动 github-hosts 代理
                proxy = GithubHostsProxy()
                if not proxy.start():
                    logging.warning("github-hosts 代理启动失败，尝试直连下载")
                else:
                    # 配置 RequestClient 使用本地代理
                    RequestClient.get_instance().client.proxies.update({
                        'http': proxy.proxy_url,
                        'https': proxy.proxy_url,
                    })

                # 2. 下载更新文件到临时目录
                temp_dir = tempfile.mkdtemp(prefix='qsbeanfun_update_')
                download_win.set_status("正在连接服务器...")
                # 连接前再次检查取消标志
                if cancel_event.is_set():
                    raise _UpdateCancelled()
                # 在辅助线程中发起连接请求，主线程轮询取消标志，实现连接阶段可中断
                fetch_result = {}

                def _fetch():
                    try:
                        fetch_result['resp'] = RequestClient.get_instance().get(
                            download_url, stream=True, timeout=(5, 120))
                    except Exception as e:
                        fetch_result['error'] = e

                fetch_thread = threading.Thread(target=_fetch, daemon=True)
                fetch_thread.start()
                while fetch_thread.is_alive():
                    if cancel_event.is_set():
                        raise _UpdateCancelled()
                    time.sleep(0.1)
                # 连接线程结束，检查结果
                if 'error' in fetch_result:
                    raise fetch_result['error']
                response = fetch_result['resp']
                # 连接返回后再次检查取消标志
                if cancel_event.is_set():
                    raise _UpdateCancelled()
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                start_time = time.time()

                if update_type == 'incremental':
                    # 增量更新：只下载 Beanfun.exe
                    download_win.set_status("正在下载更新程序...")
                    exe_path = os.path.join(temp_dir, 'Beanfun.exe')
                    with open(exe_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if cancel_event.is_set():
                                raise _UpdateCancelled()
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total_size > 0:
                                    percent = int(downloaded * 100 / total_size)
                                    download_win.set_progress(percent)
                                    elapsed = time.time() - start_time
                                    if elapsed > 0:
                                        speed = downloaded / elapsed / 1024  # KB/s
                                        download_win.set_speed(f"{speed:.1f} KB/s")
                    logging.info(f"增量更新包下载完成: {exe_path}")
                    # 生成增量更新脚本（只替换 exe）
                    download_win.set_status("正在准备重启...")
                    UpdaterClient.__run_update_script(exe_path, temp_dir, incremental=True)
                else:
                    # 全量更新：下载 QsBeanfun.zip 并解压
                    download_win.set_status("正在下载更新包...")
                    zip_path = os.path.join(temp_dir, 'QsBeanfun.zip')
                    with open(zip_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if cancel_event.is_set():
                                raise _UpdateCancelled()
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total_size > 0:
                                    percent = int(downloaded * 100 / total_size)
                                    download_win.set_progress(percent)
                                    elapsed = time.time() - start_time
                                    if elapsed > 0:
                                        speed = downloaded / elapsed / 1024  # KB/s
                                        download_win.set_speed(f"{speed:.1f} KB/s")
                    logging.info(f"更新包下载完成: {zip_path}")

                    # 解压
                    download_win.set_status("正在解压更新包...")
                    extract_dir = os.path.join(temp_dir, 'extract')
                    with zipfile.ZipFile(zip_path, 'r') as zf:
                        zf.extractall(extract_dir)
                    logging.info(f"更新包解压完成: {extract_dir}")

                    # 生成全量更新脚本（xcopy 替换）
                    download_win.set_status("正在准备重启...")
                    UpdaterClient.__run_update_script(extract_dir, temp_dir, incremental=False)
                return None
            except _UpdateCancelled:
                logging.info("用户取消更新")
                return None
            except Exception as e:
                logging.error(f"自动更新失败: {str(e)}")
                return f"自动更新失败：{str(e)}\n请前往 GitHub 手动下载"

        def __update_result(window, result, e):
            # 关闭下载进度窗口
            download_win.close()
            # 停止 github-hosts 代理，避免资源泄漏
            if proxy is not None:
                try:
                    proxy.stop()
                except Exception as ex:
                    logging.warning(f"停止 github-hosts 代理失败: {str(ex)}")
            if result:
                BoxPop.err(window, result)

        get_thread_pool().submit_task(__do_update, __update_result, window, show_loading=False)

    @staticmethod
    def __run_update_script(source: str, temp_dir: str, incremental: bool = False):
        """生成更新脚本，等待主程序退出后替换文件并重启。

        Args:
            source: 增量模式为新的 Beanfun.exe 路径；全量模式为解压目录
            temp_dir: 临时目录（脚本执行后清理）
            incremental: True 表示增量更新（只替换 exe），False 表示全量更新（xcopy 替换）
        """
        try:
            # 当前程序路径
            if getattr(sys, 'frozen', False):
                app_dir = os.path.dirname(sys.executable)
                app_exe = sys.executable
            else:
                app_dir = build_path('')
                app_exe = sys.executable

            # 生成更新脚本
            script_path = os.path.join(temp_dir, 'update.bat')
            if incremental:
                # 增量更新：只替换 Beanfun.exe
                script_content = f"""@echo off
chcp 65001 >nul
echo 正在等待程序退出...
:wait
tasklist /FI "IMAGENAME eq {os.path.basename(app_exe)}" 2>nul | find /I "{os.path.basename(app_exe)}" >nul
if %errorlevel%==0 (
    timeout /t 1 /nobreak >nul
    goto wait
)
echo 正在替换程序...
copy /Y "{source}" "{app_exe}" >nul
echo 替换完成，正在重新启动...
start "" "{app_exe}"
echo 清理临时文件...
rd /S /Q "{temp_dir}"
exit
"""
            else:
                # 全量更新：xcopy 替换整个目录
                script_content = f"""@echo off
chcp 65001 >nul
echo 正在等待程序退出...
:wait
tasklist /FI "IMAGENAME eq {os.path.basename(app_exe)}" 2>nul | find /I "{os.path.basename(app_exe)}" >nul
if %errorlevel%==0 (
    timeout /t 1 /nobreak >nul
    goto wait
)
echo 正在替换文件...
xcopy /E /Y /Q "{source}" "{app_dir}" >nul
echo 替换完成，正在重新启动...
start "" "{app_exe}"
echo 清理临时文件...
rd /S /Q "{temp_dir}"
exit
"""
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # 启动更新脚本（独立进程）
            subprocess.Popen(
                ['cmd', '/c', script_path],
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                close_fds=True
            )

            # 退出当前程序
            logging.info("更新脚本已启动，正在退出当前程序")
            os._exit(0)
        except Exception as e:
            logging.error(f"生成更新脚本失败: {str(e)}")
            raise
