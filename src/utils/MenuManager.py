import logging
import subprocess
import sys
import typing
import webbrowser

from PyQt5.QtWidgets import (QMenu, QAction)

from src.client import QsClient, RequestClient
from src.config.GlobalConfig import GLOBAL_CONFIG
from src.models.CustomMenu import CustomMenu
from src.utils import BoxPop, SystemCom, BaseTools, WinManager
from src.utils.ThreadTools import CustomThread
from src.window import PyQtBrowser
from src.window.AboutWin import AboutWin
from src.window.AccountInfoWin import AccountInfoWin
from src.window.MainWin import MainWin
from src.window.QrCodeShowWin import QrCodeShowWin


def init_menu(self):
    menu_config = [
        CustomMenu(name="user_center", title="用户中心", children=[
            CustomMenu(name="user_center_member", title="会员中心",
                       handler=lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_member_center(GLOBAL_CONFIG.bf_web_token), self)),
            CustomMenu(name="user_center_recharge", title="储值中心",
                       handler=lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_user_recharge(GLOBAL_CONFIG.bf_web_token), self)),
            CustomMenu(name="user_center_service", title="客服中心", handler=lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_service_center(), self)),
            CustomMenu(name="user_center_account_info", title="账号详情", handler=lambda: user_info_triggered(self)),
            CustomMenu(name="user_center_login_out", title="登出", handler=lambda: user_loginOut_triggerd(self)),
        ]),
        CustomMenu(name="tools", title="实用工具", children=[
            CustomMenu(name="tools_hexa", title="Hexa计算器", handler=lambda: PyQtBrowser.open_browser('https://starmcc.github.io/MapleStoryCoreCalc/', self)),
            CustomMenu(name="tools_star", title="星力模拟器", handler=lambda: PyQtBrowser.open_browser('https://maplehexa.cisyy.cc/starforceEmulator/', self)),
            CustomMenu(name="tools_all_tools", title="枫之谷小工具", handler=lambda: PyQtBrowser.open_browser('https://mstoolbox.netlify.app/', self)),
            CustomMenu(name="tools_union", title="联盟摆放模拟器", handler=lambda: PyQtBrowser.open_browser('https://xenogents.github.io/LegionSolver/', self)),
            CustomMenu(name="tools_paper_dolls", title="开源纸娃娃系统", handler=lambda: webbrowser.open('https://github.com/Elem8100/MapleNecrocer')),
            CustomMenu(name="tools_exchange", title="汇率换算", handler=lambda: PyQtBrowser.open_browser('https://zh.coinmill.com/CNY_calculator.html', self)),
            CustomMenu(name="tools_calc", title="系统计算器", handler=lambda: subprocess.Popen('calc.exe')),
        ]),
        CustomMenu(name="func", title="实用功能", children=[
            CustomMenu(name="func_ngs_kill", title="强制结束NGS进程", handler=lambda: tools_ngsKill_triggered(self)),
            CustomMenu(name="func_game_kill", title="强制结束游戏", handler=lambda: tools_gameKill_triggered(self)),
        ]),
        CustomMenu(name="about", title="关于作者..", handler=lambda: help_open_about_triggered(self)),
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


def build_dynamic_menu(window, menu: QMenu):
    def __build_result(data):
        entry, win = data
        logging.error(f"測試={entry}")
        submenu = QMenu(WinManager.translate("便捷导航"), win)
        submenu.setObjectName("nav")
        actions = menu.actions()
        index = len(actions) - 3
        index = index if index > 0 else 0
        menu.insertMenu(actions[index], submenu)
        if entry:
            __build_dynamic_menu(win, entry, submenu)
        action = QAction(WinManager.translate("更新导航数据"), submenu)
        action.setObjectName("nav_update_list")

        def re_deleteLater():
            submenu.deleteLater()
            build_dynamic_menu(win, menu)
            return

        action.triggered.connect(re_deleteLater)
        submenu.addAction(action)

    CustomThread.run_task(__get_dynamic_menu_config, __build_result, None, window=window)


def __get_dynamic_menu_config(window) -> typing.Any:
    # 先读取网络配置，再进行菜单配置
    try:
        response = RequestClient.get_instance().get("https://gitee.com/starmcc/qs-beanfun-menu/raw/master/config.json")
        if response.status_code != 200:
            return None, window
        try:
            # 解析JSON响应
            entry = response.json()
        except ValueError as e:
            logging.error(f"JSON解析失败:\n{str(e)}")
            return None, window
            # 检查响应数据结构完整性
        if not isinstance(entry, list):
            logging.error("获取二维码失败,错误代码[0]")
            return None, window
        return entry, window
    except Exception as e:
        logging.error(f"请求出错 error{str(e)}")
        return None, window


def __build_dynamic_menu(self, entry, nav_menu: QMenu):
    # title = 菜单名称
    # data = 数据
    for item in entry:
        if not isinstance(item, dict):
            continue

        name = item.get('name')
        title = WinManager.translate(item.get('title'))
        type = int(item.get('type'))
        data = item.get('data')

        if isinstance(data, list):
            submenu = nav_menu.addMenu(title)
            submenu.setObjectName(name)
            __build_dynamic_menu(self, data, submenu)
            continue
        else:
            action = QAction(title, nav_menu)
            action.setObjectName(name)

        if type == 1:
            # type 1 = 浏览器跳转链接
            def go(s, data=data):
                webbrowser.open(data)

            action.triggered.connect(go)
        elif type == 2:
            # type  2 = 内置浏览器访问
            def go(s, data=data, self=self):
                PyQtBrowser.open_browser(data, self)

            action.triggered.connect(go)
        elif type == 3:
            # type  3 = 二维码页面
            def goto_qr_page(s, data=data, title=title):
                win = QrCodeShowWin(self, title, data)
                win.show()

            action.triggered.connect(goto_qr_page)
        nav_menu.addAction(action)


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
    GLOBAL_CONFIG.win_accountInfo.notice_refresh.connect(self.get_account_info_clicked)
    GLOBAL_CONFIG.win_accountInfo.exec_()
