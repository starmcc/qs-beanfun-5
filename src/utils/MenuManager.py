import subprocess
import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from src.client import QsClient
from src.config.GlobalConfig import GLOBAL_CONFIG
from src.models.CustomMenu import CustomMenu
from src.utils import BoxPop, SystemCom, BaseTools
from src.window.MainWin import MainWin
from src.window import PyQtBrowser


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
        CustomMenu(name="nav", title="便捷导航", handler=lambda: open_win(self, "nav")),
        CustomMenu(name="config", title="设置", handler=lambda: open_win(self,"config")),
        CustomMenu(name="about", title="关于作者..", handler=lambda: open_win(self, "about")),
        CustomMenu(name="check_update", title="检测更新", handler=lambda: BaseTools.check_new_version(self, False)),
        CustomMenu(name="out", title="退出", handler=sys.exit),
    ]

    # 创建菜单
    title_menu = QMenu(self)
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
            submenu = menu.addMenu(item.title)
            submenu.setObjectName(item.name)
            __build_menu(window, submenu, item.children)
        else:
            # 创建普通菜单项
            action = QAction(item.title, menu)
            action.setObjectName(item.name)
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