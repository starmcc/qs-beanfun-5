import importlib
import logging
import os
import shutil
import sys
import webbrowser
from typing import Tuple

from PySide6.QtWidgets import QMessageBox
from packaging import version

from src.client import RequestClient
from src.config import Config
from src.config.GlobalConfig import GlobalConstants
from src.utils import BoxPop
from src.utils.ThreadPoolManager import get_thread_pool


def hidden_str(s):
    if s and len(s) > 5:
        return s[:5] + '*' * (len(s) - 5)
    else:
        return s


def build_path(path: str):
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        p = os.path.dirname(sys.executable)
        return rf'{p}\{path}'
    # 如果是在开发环境中运行
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    return rf'{p}\{path}'


def check_new_version(win, quiet: bool = True):
    # 如果是安静模式,且无勾选检查更新
    if quiet and not Config.app_check_update():
        return

    # 检查更新
    def __check_update_result(window, result, e):
        if not result:
            result = (False, '未知错误')
        status_flag, message = result
        if e:
            logging.error(f"检查版本更新出现错误：\n {str(e)}")
            status_flag = False
            message = "无法获取版本信息"
        if status_flag:
            # 修复：ButtonRole 枚举前缀
            buttons = {
                "前往更新": QMessageBox.ButtonRole.AcceptRole,
                "取消": QMessageBox.ButtonRole.RejectRole
            }
            if quiet:
                buttons = {
                    "前往更新": QMessageBox.ButtonRole.AcceptRole,
                    "不再提醒": QMessageBox.ButtonRole.ActionRole,
                    "取消": QMessageBox.ButtonRole.RejectRole
                }
            click_result = BoxPop.custom_question(window, message, buttons)

            if click_result == QMessageBox.ButtonRole.AcceptRole:
                webbrowser.open(f"{GlobalConstants.GITHUB_URL}/releases")
            if quiet and click_result == QMessageBox.ButtonRole.ActionRole:
                Config.app_check_update(False)
        elif not quiet:
            BoxPop.info(window, message)

    get_thread_pool().submit_task(__check_version, __check_update_result, win, not quiet)


def __check_version() -> Tuple[bool, str]:
    # bool = 是否有更新
    # str = 更新内容,错误消息
    msg = '无法获取版本信息'
    response = RequestClient.get_instance().get(f"{GlobalConstants.GITHUB_API_URL}/releases/latest")
    response.raise_for_status()
    data = response.json()
    latest_version = data.get('tag_name')
    if latest_version is None:
        return False, msg
    if version.parse(GlobalConstants.APP_VERSION) >= version.parse(latest_version):
        return False, '当前是最新版本'
    else:
        body = data.get('body')
        msg = f'发现新版本：{latest_version}\n{body}\n是否前往更新?'
        return True, msg


def build_chrome():
    """将 QtWebEngineProcess.exe 复制为 chrome.exe，使游戏加速器识别为浏览器进程并放行流量。
    兼容开发环境（PySide6 site-packages）和 PyInstaller 打包后（_internal 目录）两种场景。"""
    # 优先查找 PySide6 中的 QtWebEngineProcess.exe
    spec = importlib.util.find_spec('PySide6')
    if spec and spec.submodule_search_locations:
        pyside6_dir = spec.submodule_search_locations[0]
        source_path = os.path.join(pyside6_dir, 'QtWebEngineProcess.exe')
    else:
        # PyInstaller 打包后：QtWebEngineProcess.exe 在 _internal 目录
        base_dir = os.path.dirname(sys.executable)
        source_path = os.path.join(base_dir, '_internal', 'QtWebEngineProcess.exe')

    if not os.path.exists(source_path):
        logging.warning(f"未找到 QtWebEngineProcess.exe: {source_path}")
        return None

    target_path = os.path.join(os.path.dirname(source_path), 'chrome.exe')
    if os.path.exists(target_path):
        logging.info(f"chrome.exe 已存在: {target_path}")
        return target_path

    try:
        shutil.copy2(source_path, target_path)
        logging.info(f"已创建 chrome.exe: {target_path}")
        return target_path
    except Exception as e:
        logging.error(f"创建 chrome.exe 失败: {e}")
        return None


def check_cn_path(path):
    if not path:
        return False
    for char in path:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False