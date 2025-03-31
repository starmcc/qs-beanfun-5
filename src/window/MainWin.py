import logging
import math
import subprocess
import sys
import webbrowser
from decimal import Decimal

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from src.client import QsClient
from src.config import Config
from src.config.GlobalConfig import GLOBAL_CONFIG, GLOBAL_PATH_PLUGIN_ZWW_ZIP
from src.models.Account import Account
from src.utils import BaseTools, SystemCom, BoxPop, SchedulerManager
from src.utils.TaskQueue import TaskQueue
from src.utils.ThreadTools import CustomThread
from src.views.Ui_Main import Ui_Main
from src.window import PyQtBrowser
from src.window.AboutWin import AboutWin
from src.window.AccountInfoWin import AccountInfoWin
from src.window.ConfigWin import ConfigWin
from src.window.LoadMask import LoadMask
from src.window.TrayIcon import TrayIcon


class MainWin(QMainWindow, Ui_Main):
    icon: TrayIcon
    nowAccount: Account = Account()
    task_id: str

    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_queue = TaskQueue()
        self.setupUi(self)
        BaseTools.set_basic_window(self)
        self.children_accounts: list[Account] = []
        self.auth_cert = True
        self.init_ui()
        self.get_account_info()
        self.refresh_points()
        # 定时心跳保证登录状态
        self.task_id = SchedulerManager.do_task(self.refresh_login_status, 1000 * 60 * 5)

    def closeEvent(self, a0):
        # 当窗口关闭时停止心跳
        SchedulerManager.stop_task(self.task_id)
        self.icon.deleteLater()
        super().closeEvent(a0)

    def refresh_login_status(self, task_id):
        QsClient.get_instance().heartbeat()

    def init_ui(self):
        self.icon = TrayIcon(self)
        self.checkBox_autoInput.setChecked(Config.auto_input())
        self.pushButton_dynamicPwd.clicked.connect(self.dynamicPwd_clicked)
        self.pushButton_start.clicked.connect(self.start_clicked)
        self.pushButton_config.clicked.connect(self.config_clicked)
        self.pushButton_createAct.clicked.connect(self.createAct_clicked)
        self.pushButton_loginOut.clicked.connect(self.user_loginOut_triggerd)
        self.lineEdit_numAct.installEventFilter(self)  # 安装事件过滤器
        self.lineEdit_dynamicPwd.installEventFilter(self)
        self.checkBox_autoInput.stateChanged.connect(self.autoInput_stateChanged)
        self.comboBox_gameAct.currentIndexChanged.connect(self.refresh_account_info)
        self.label_points.mousePressEvent = self.refresh_points
        self.label_status.mousePressEvent = self.get_account_info
        self.__init_menu()
        self.pushButton_loginOut.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.lineEdit_numAct:
            if event.type() == QEvent.HoverEnter:
                self.lineEdit_numAct.setText(self.nowAccount.id)
            elif event.type() == QEvent.HoverLeave:
                self.lineEdit_numAct.setText(BaseTools.hidden_str(self.nowAccount.id))
        elif obj == self.lineEdit_dynamicPwd:
            if event.type() == QEvent.HoverEnter:  # 获取焦点事件
                self.lineEdit_dynamicPwd.setText(self.nowAccount.dynamic_pwd)
            elif event.type() == QEvent.HoverLeave:  # 失去焦点事件
                self.lineEdit_dynamicPwd.setText(BaseTools.hidden_str(self.nowAccount.dynamic_pwd))

        return super().eventFilter(obj, event)

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.hide()

    def createAct_clicked(self):
        if not self.auth_cert:
            BoxPop.info(self, '此账号尚未完成进阶认证,请前往会员中心完成后重新登录!')
            return
        text, ok = BoxPop.input_dialog(self, '新建账号', '请输入账号名称')
        if not ok or not text:
            return

        try:
            status, msg = QsClient.get_instance().add_account(text)
            if not status:
                BoxPop.err(self, msg)
            else:
                BoxPop.info(self, msg)
            self.get_account_info()
        except Exception as e:
            logging.error(e)
            BoxPop.info(self, '操作异常！')

    def autoInput_stateChanged(self):
        Config.auto_input(self.checkBox_autoInput.isChecked())

    def dynamicPwd_clicked(self):
        try:
            self.nowAccount.dynamic_pwd = QsClient.get_instance().get_dynamic_password(self.children_accounts[0], GLOBAL_CONFIG.bf_web_token)
            self.lineEdit_dynamicPwd.setText(self.nowAccount.dynamic_pwd)
        except Exception as e:
            logging.error(e)
            BoxPop.err(self, '可能由于网络原因导致请求动态密令失败!\n也可能是无进阶认证导致获取失败!')
        try:
            # 需要运行游戏才能执行自动输入
            if self.checkBox_autoInput.isChecked() and SystemCom.check_game_running():
                SystemCom.auto_input_act_pwd(self.nowAccount.id, self.nowAccount.dynamic_pwd)
        except Exception as e:
            logging.error(e)
            BoxPop.err(self, '自动输入失败,请手动输入!')

    def start_clicked(self):
        try:
            SystemCom.run_game(self, self.lineEdit_numAct.text(), self.lineEdit_dynamicPwd.text(), self.run_game_result)
        except Exception as e:
            logging.error(e)
            BoxPop.err(self, '启动异常!')

    def run_game_result(self, data):
        status, msg = data
        # -1 = 异常
        # 1  = 设置游戏目录
        # 2  = 免输入模式错误
        # 3  = 自动阻止更新成功
        # 4  = 自动阻止更新失败
        if status == 0 or status == -1 or status == 2 or status == 4:
            logging.error(msg)
            BoxPop.err(self, msg)
        elif status == 1:
            if not BoxPop.question(self, msg):
                return
            options = QFileDialog.Options()
            directory = QFileDialog.getExistingDirectory(None, "请选择新枫之谷游戏目录", "", options=options)
            if not directory:
                return
            Config.game_path(directory)
            # 重新打开
            self.start_clicked()
        elif status == 3:
            BoxPop.info(self, msg)

    def get_account_info(self, event=None):
        """
        获取账号信息
        """
        try:
            result = QsClient.get_instance().get_account_list(GLOBAL_CONFIG.bf_web_token)
            self.children_accounts = result.accounts
            self.auth_cert = result.auth_cert
            self.comboBox_gameAct.clear()
            self.pushButton_createAct.setVisible(result.new_user)
            self.pushButton_dynamicPwd.setEnabled(not result.new_user)
            self.lineEdit_numAct.setText('')
            self.lineEdit_dynamicPwd.setText('')
            if result.new_user is True or len(self.children_accounts) == 0:
                # 新账号
                if not self.auth_cert:
                    BoxPop.info(self, '此账号尚未完成电话进阶认证\n请前往会员中心完成后重新登录！')
                    # 不允许创建账号和查看账号详情
                    self.pushButton_createAct.setEnabled(False)
                    self.action_user_info.setEnabled(False)
                return
            for entry in self.children_accounts:
                self.comboBox_gameAct.addItem(entry.name, userData=entry.id)
            self.comboBox_gameAct.setCurrentIndex(0)
            self.nowAccount = self.children_accounts[0]
            self.refresh_account_info(0)
        except Exception as e:
            logging.error(e)
            BoxPop.err(self, '获取账号信息失败!')

    def refresh_account_info(self, index):
        """
        刷新账号信息
        """
        item = self.comboBox_gameAct.itemData(index)
        for i, entry in enumerate(self.children_accounts):
            # 清空动态密码
            entry.dynamic_pwd = ''
            if entry.id == item:
                self.nowAccount = entry
                break
            if i == len(self.children_accounts) - 1:
                return
        palette = self.label_status.palette()
        if self.nowAccount.status:
            self.label_status.setText('正常')
            palette.setColor(QPalette.WindowText, QColor(0, 0, 255))
        else:
            self.label_status.setText('禁止')
            palette.setColor(QPalette.WindowText, QColor(255, 0, 0))
        self.label_status.setPalette(palette)
        self.lineEdit_numAct.setText(BaseTools.hidden_str(self.nowAccount.id))
        self.lineEdit_dynamicPwd.setText('')

    def config_clicked(self):
        GLOBAL_CONFIG.win_config = ConfigWin(self)
        GLOBAL_CONFIG.win_config.exec_()

    def refresh_points(self, event=None):
        def __task():
            try:
                points = QsClient.get_instance().get_game_points(GLOBAL_CONFIG.bf_web_token)
                points_game = math.floor(Decimal(points) / Decimal('2.5'))
                template = f"{points}[{points_game}]"
                self.label_points.setText(template)
            except Exception as e:
                logging.error(e)

        CustomThread.run_task(__task, None, LoadMask(self))

    ## ----------------------- 菜单事件 -----------------------

    def __init_menu(self):
        # 用户中心
        self.action_user_center.triggered.connect(lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_member_center(GLOBAL_CONFIG.bf_web_token), self))
        self.action_user_recharge.triggered.connect(lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_user_recharge(GLOBAL_CONFIG.bf_web_token), self))
        self.action_user_services.triggered.connect(lambda: PyQtBrowser.open_browser(QsClient.get_instance().get_web_url_service_center(), self))
        self.action_user_info.triggered.connect(self.user_info_triggered)
        self.action_user_loginOut.triggered.connect(self.user_loginOut_triggerd)
        self.action_user_exit.triggered.connect(sys.exit)
        # 快速导航
        self.action_nav_mapleStory.triggered.connect(lambda: webbrowser.open('https://maplestory.beanfun.com/main'))
        self.action_nav_gamana_hk.triggered.connect(lambda: webbrowser.open('https://bfweb.hk.beanfun.com/'))
        self.action_nav_gamana_tw.triggered.connect(lambda: webbrowser.open('https://tw.beanfun.com'))
        self.action_nav_tb_beanfun.triggered.connect(lambda: webbrowser.open('https://tieba.baidu.com/f?kw=beanfun'))
        self.action_nav_tb_xfzg.triggered.connect(lambda: webbrowser.open('https://tieba.baidu.com/f?kw=%E6%96%B0%E6%9E%AB%E4%B9%8B%E8%B0%B7'))
        self.action_nav_bahamute.triggered.connect(lambda: webbrowser.open('https://forum.gamer.com.tw/A.php?bsn=7650/'))
        self.action_nav_toushijing.triggered.connect(lambda: webbrowser.open('http://www.gametsg.com/maplestory/'))
        self.action_nav_author_bilibili.triggered.connect(lambda: webbrowser.open('https://space.bilibili.com/391919722'))

        # 实用功能
        self.action_tools_ngsKill.triggered.connect(self.tools_ngsKill_triggered)
        self.action_tools_sysCalc.triggered.connect(lambda: subprocess.Popen('calc.exe'))
        self.action_tools_minCoreCalc.triggered.connect(lambda: PyQtBrowser.open_browser('https://starmcc.github.io/MapleStoryCoreCalc/', self))
        self.action_tools_huilv.triggered.connect(lambda: PyQtBrowser.open_browser('https://zh.coinmill.com/CNY_calculator.html', self))
        self.action_tools_lianMeng.triggered.connect(lambda: PyQtBrowser.open_browser('https://starmcc.github.io/MapleStoryAllianceSimulator/', self))
        self.action_tools_zww.triggered.connect(self.tools_zww_triggered)

        # Help
        self.action_help_about.triggered.connect(self.help_open_about_triggered)
        self.action_help_update.triggered.connect(lambda: BaseTools.check_version(self))

    def tools_zww_triggered(self):
        plugin_directory = BaseTools.extract_build_plugin(GLOBAL_PATH_PLUGIN_ZWW_ZIP)
        subprocess.Popen(rf'{plugin_directory}\MapleNecrocer.exe')

    def tools_ngsKill_triggered(self):
        if BoxPop.question(self, '是否立即结束NGS进程？'):
            err = SystemCom.kill_black_xchg()
            if err:
                BoxPop.err(self, err)

    def user_loginOut_triggerd(self):
        from src.window.LoginWin import LoginWin
        QsClient.get_instance().login_out()
        win_login = LoginWin()
        self.close()

    def user_info_triggered(self):
        GLOBAL_CONFIG.win_accountInfo = AccountInfoWin(self, self.nowAccount)
        GLOBAL_CONFIG.win_accountInfo.notice_refresh.connect(self.get_account_info)
        GLOBAL_CONFIG.win_accountInfo.exec_()

    def help_open_about_triggered(self):
        GLOBAL_CONFIG.win_about = AboutWin(self)
        GLOBAL_CONFIG.win_about.exec_()

    ## ----------------------- 菜单End -----------------------
