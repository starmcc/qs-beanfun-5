import subprocess
import sys
import webbrowser

from PyQt5.QtWidgets import (QMenu, QAction)

from src.client import QsClient
from src.config.GlobalConfig import GLOBAL_CONFIG
from src.models.CustomMenu import CustomMenu
from src.utils import BoxPop, SystemCom, BaseTools
from src.window import PyQtBrowser
from src.window.AboutWin import AboutWin
from src.window.AccountInfoWin import AccountInfoWin
from src.window.MainWin import MainWin


def init_menu(self):
    menu_config = [
        CustomMenu(menu_id=0, title="用户中心", children=[
            CustomMenu(menu_id=0, title="会员中心", handler=lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_member_center(GLOBAL_CONFIG.bf_web_token), self)),
            CustomMenu(menu_id=0, title="储值中心", handler=lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_user_recharge(GLOBAL_CONFIG.bf_web_token), self)),
            CustomMenu(menu_id=0, title="客服中心", handler=lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_service_center(), self)),
            CustomMenu(menu_id=0, title="账号详情", handler=lambda: user_info_triggered(self)),
            CustomMenu(menu_id=0, title="登出", handler=lambda: user_loginOut_triggerd(self)),
        ]),
        CustomMenu(menu_id=1, title="快速导航", children=[
            CustomMenu(menu_id=1, title="新枫之谷官网", handler=lambda: webbrowser.open('https://maplestory.beanfun.com/main')),
            CustomMenu(menu_id=1, title="游戏橘子官网", children=[
                CustomMenu(menu_id=1, title="香港地区", handler=lambda: webbrowser.open('https://bfweb.hk.beanfun.com/')),
                CustomMenu(menu_id=1, title="台湾地区", handler=lambda: webbrowser.open('https://tw.beanfun.com/')),
            ]),
            CustomMenu(menu_id=1, title="百度贴吧", children=[
                CustomMenu(menu_id=1, title="Beanfun贴吧", handler=lambda: webbrowser.open('https://tieba.baidu.com/f?kw=beanfun')),
                CustomMenu(menu_id=1, title="新枫之谷贴吧", handler=lambda: webbrowser.open('https://tieba.baidu.com/f?kw=%E6%96%B0%E6%9E%AB%E4%B9%8B%E8%B0%B7')),
            ]),
            CustomMenu(menu_id=1, title="巴哈姆特", handler=lambda: webbrowser.open('https://forum.gamer.com.tw/B.php?bsn=7650')),
            CustomMenu(menu_id=1, title="作者B站", handler=lambda: webbrowser.open('https://space.bilibili.com/391919722')),
        ]),
        CustomMenu(menu_id=2, title="实用工具", children=[
            CustomMenu(menu_id=2, title="强制结束NGS进程", handler=lambda: tools_ngsKill_triggered(self)),
            CustomMenu(menu_id=2, title="Hexa计算器", handler=lambda: PyQtBrowser.open_browser('https://starmcc.github.io/MapleStoryCoreCalc/', self)),
            CustomMenu(menu_id=2, title="星力模拟器", handler=lambda: PyQtBrowser.open_browser('https://maplehexa.cisyy.cc/starforceEmulator/', self)),
            CustomMenu(menu_id=2, title="枫之谷小工具", handler=lambda: PyQtBrowser.open_browser('https://mstoolbox.netlify.app/', self)),
            CustomMenu(menu_id=2, title="联盟摆放模拟器", handler=lambda: PyQtBrowser.open_browser('https://xenogents.github.io/LegionSolver/', self)),
            CustomMenu(menu_id=2, title="开源纸娃娃系统", handler=lambda: webbrowser.open('https://github.com/Elem8100/MapleNecrocer')),
            CustomMenu(menu_id=2, title="汇率换算", handler=lambda: PyQtBrowser.open_browser('https://zh.coinmill.com/CNY_calculator.html', self)),
            CustomMenu(menu_id=2, title="系统计算器", handler=lambda: subprocess.Popen('calc.exe')),
        ]),
        CustomMenu(menu_id=3, title="关于作者..", handler=lambda: help_open_about_triggered(self)),
        CustomMenu(menu_id=3, title="检测更新", handler=lambda: BaseTools.check_version(self)),
        CustomMenu(menu_id=999, title="退出", handler=sys.exit),
    ]

    # 创建菜单
    title_menu = QMenu(self)

    # 递归生成菜单项
    def build_menu(menu: QMenu, config_items: list):
        for item in config_items:
            if item.menu_id == 0:
                if not isinstance(self, MainWin):
                    continue
            if item.children:
                # 创建子菜单
                submenu = menu.addMenu(item.title)
                build_menu(submenu, item.children)
            else:
                # 创建普通菜单项
                action = QAction(item.title, menu)
                if item.handler:
                    action.triggered.connect(item.handler)
                menu.addAction(action)

    # 构建主菜单
    build_menu(title_menu, menu_config)
    return title_menu


# =======================
def tools_ngsKill_triggered(self):
    if BoxPop.question(self, '是否立即结束NGS进程？'):
        err = SystemCom.kill_black_xchg()
        if err:
            BoxPop.err(self, err)


def help_open_about_triggered(self):
    GLOBAL_CONFIG.win_about = AboutWin(self)
    GLOBAL_CONFIG.win_about.exec_()


def user_loginOut_triggerd(self):
    from src.window.LoginWin import LoginWin
    QsClient.get_instance().login_out()
    win_login = LoginWin()
    win_login.show()
    self.close()


def user_info_triggered(self):
    GLOBAL_CONFIG.win_accountInfo = AccountInfoWin(self, self.nowAccount)
    GLOBAL_CONFIG.win_accountInfo.notice_refresh.connect(self.get_account_info)
    GLOBAL_CONFIG.win_accountInfo.exec_()
