import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from src.client import RequestClient
from src.config.StyleConstants import StyleConstants
from src.client import QsClient
from src.config.GlobalConfig import GLOBAL_CONFIG
from src.models.CustomMenu import CustomMenu
from src.utils import BoxPop, SystemCom, BaseTools
from src.config.I18n import tr
from src.utils.ThreadPoolManager import get_thread_pool
from src.window.MainWin import MainWin
from src.components import PyQtBrowser


def init_menu(self):
    menu_config = [
        CustomMenu(name="run_game", title="启动游戏", handler=lambda: SystemCom.run_game(self)),
        CustomMenu(name="user_center", title="用户中心", children=[
            CustomMenu(name="user_center_member", title="会员中心",
                       handler=lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_member_center(GLOBAL_CONFIG.bf_web_token), self)),
            CustomMenu(name="user_center_recharge", title="储值中心",
                       handler=lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_user_recharge(GLOBAL_CONFIG.bf_web_token), self)),
            CustomMenu(name="user_center_service", title="客服中心", handler=lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_service_center(), self)),
            CustomMenu(name="user_center_account_info", title="账号详情", handler=lambda: open_win(self,"userInfo")),
            CustomMenu(name="user_center_login_out", title="登出", handler=lambda: user_loginOut_triggerd(self)),
        ]),
        CustomMenu(name="func", title="实用功能", children=[
            CustomMenu(name="func_ngs_kill", title="强制结束NGS进程", handler=lambda: tools_ngsKill_triggered(self)),
            CustomMenu(name="func_game_kill", title="强制结束游戏", handler=lambda: tools_gameKill_triggered(self)),
            CustomMenu(name="tools_calc", title="系统计算器", handler=lambda: subprocess.Popen('calc.exe')),
        ]),
        CustomMenu(name="classic", title="经典版", children=[
            CustomMenu(name="classic_download_ngm", title="下载GGM插件", handler=lambda: classic_download_ngm(self)),
            CustomMenu(name="classic_install", title="安装枫之谷经典版", handler=lambda: classic_install(self)),
        ]),
        CustomMenu(name="nav", title="便捷导航", handler=lambda: open_win(self, "nav")),
        CustomMenu(name="config", title="设置", handler=lambda: open_win(self,"config")),
        CustomMenu(name="check_update", title="获取新版本", handler=lambda: BaseTools.check_new_version(self, False)),
        CustomMenu(name="about", title="关于..", handler=lambda: open_win(self, "about")),
        CustomMenu(name="out", title="退出", handler=sys.exit),
    ]

    # 创建菜单
    title_menu = QMenu(self)
    title_menu.setStyleSheet(StyleConstants.MENU_STYLE)
    # 构建主菜单
    __build_menu(self, title_menu, menu_config)
    return title_menu


# 递归生成菜单项
def __build_menu(window, menu: QMenu, config_items: list):
    for item in config_items:
        if item.name == 'user_center':
            if not isinstance(window, MainWin):
                continue
        if item.children:
            # 创建子菜单
            submenu = menu.addMenu(tr(item.title))
            submenu.setObjectName(item.name)
            submenu.setProperty('_i18n_source_title', item.title)
            __build_menu(window, submenu, item.children)
        else:
            # 创建普通菜单项
            action = QAction(tr(item.title), menu)
            action.setObjectName(item.name)
            action.setProperty('_i18n_source_text', item.title)
            if item.handler:
                action.triggered.connect(item.handler)
            menu.addAction(action)


# =======================
def tools_ngsKill_triggered(self):
    if BoxPop.question(self, '是否立即结束Ngs进程?'):
        err = SystemCom.kill_black_xchg()
        if err:
            BoxPop.err(self, err)


def tools_gameKill_triggered(self):
    if BoxPop.question(self, '是否强制结束游戏?'):
        err = SystemCom.kill_mapleStory()
        if err:
            BoxPop.err(self, err)

def open_win(self, win_type):
    if win_type == "nav":
        from src.window.NavWin import NavWin
        GLOBAL_CONFIG.win_nav = NavWin(self)
        GLOBAL_CONFIG.win_nav.exec()
    elif win_type == "about":
        from src.window.AboutWin import AboutWin
        GLOBAL_CONFIG.win_about = AboutWin(self)
        GLOBAL_CONFIG.win_about.exec()
    elif win_type == "userInfo":
        from src.window.AccountInfoWin import AccountInfoWin
        GLOBAL_CONFIG.win_accountInfo = AccountInfoWin(self, self.nowAccount)
        GLOBAL_CONFIG.win_accountInfo.exec()
    elif win_type == "config":
        from src.window.ConfigWin import ConfigWin
        GLOBAL_CONFIG.win_config = ConfigWin(self)
        GLOBAL_CONFIG.win_config.exec()


def user_loginOut_triggerd(self):
    from src.window.LoginWin import LoginWin
    QsClient.get_instance().login_out()
    win_login = LoginWin()
    win_login.show()
    self.close()


def classic_download_ngm(self):
    """下载GGM插件 - 后台下载到临时目录并自动运行安装程序（带进度窗口）"""
    # 延迟导入，避免循环导入
    from src.window.DownloadWin import DownloadWin

    url = 'https://platform.nexon.com/NGM/Bin/Install_NGM.exe'
    tmp_dir = tempfile.gettempdir()
    tmp_file = Path(tmp_dir) / 'Install_NGM.exe'

    # 创建下载进度窗口（单独设置标题，覆盖 .ui 默认文字）
    download_win = DownloadWin(self, status="正在连接服务器...")
    download_win.set_title("正在下载GGM插件")
    download_win.show()

    # 取消标志：用户关闭窗口时置位，后台任务据此停止
    cancel_event = threading.Event()

    def __on_cancel():
        cancel_event.set()

    download_win.cancel_requested.connect(__on_cancel)

    def __download_task():
        try:
            if cancel_event.is_set():
                return None
            rsp = RequestClient.get_instance().get(url, stream=True, timeout=120)
            if rsp.status_code != 200:
                raise Exception(f'下载失败，状态码: {rsp.status_code}')
            total_size = int(rsp.headers.get('content-length', 0))
            downloaded = 0
            start_time = time.time()
            download_win.set_status("正在下载GGM插件...")
            with open(str(tmp_file), 'wb') as f:
                for chunk in rsp.iter_content(chunk_size=8192):
                    if cancel_event.is_set():
                        return None
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
            return str(tmp_file)
        except Exception as e:
            return e

    def __download_result(win, result, exception):
        # 关闭下载进度窗口
        download_win.close()
        if exception or isinstance(result, Exception):
            err = exception or result
            BoxPop.err(win, f'下载GGM插件失败:\n{str(err)}')
            return
        try:
            subprocess.Popen([result])
        except Exception as e:
            BoxPop.err(win, f'启动GGM安装程序失败:\n{str(e)}')

    get_thread_pool().submit_task(__download_task, __download_result, self, show_loading=False)


def classic_install(self):
    """安装经典版 - 通过NGM启动安装"""
    ngm_path = SystemCom.find_ngm_path()
    if not ngm_path:
        BoxPop.err(self, '未找到Nexon Game Manager安装路径，请先下载安装Nexon Game Manager插件')
        return
    try:
        subprocess.Popen([ngm_path, 'ngm://launch/%20-mode%3Ainstall%20-game%3A\'2982%402141\''])
    except Exception as e:
        BoxPop.err(self, f'启动Nexon Game Manager安装经典版失败:\n{str(e)}')