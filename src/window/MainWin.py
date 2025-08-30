import logging
import math
from decimal import Decimal
from typing import Tuple

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QFileDialog, QWidget

from src.client import QsClient
from src.config import Config
from src.config.GlobalConfig import GLOBAL_CONFIG
from src.models.Account import Account
from src.models.ActInfoResult import ActInfoResult
from src.utils import BaseTools, SystemCom, BoxPop, SchedulerManager, WinManager
from src.utils.ThreadTools import CustomThread
from src.views.Ui_Main import Ui_Main
from src.window.ConfigWin import ConfigWin
from src.window.LoadingTask import LoadingMask
from src.window.TrayIcon import TrayIcon


class MainWin(QWidget, Ui_Main):
    trayIcon: TrayIcon
    nowAccount: Account = Account()
    task_id: str

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        WinManager.set_basic_window(self)
        self.children_accounts: list[Account] = []
        self.auth_cert = True
        self.init_ui()
        self.get_account_info()
        # 定时心跳保证登录状态
        self.task_id = SchedulerManager.do_task(self.refresh_login_status, 1000 * 60 * 5)

    def closeEvent(self, a0):
        # 当窗口关闭时停止心跳
        SchedulerManager.stop_task(self.task_id)
        self.trayIcon.deleteLater()
        super().closeEvent(a0)

    def refresh_login_status(self, task_id):
        QsClient.get_instance().heartbeat()

    def init_ui(self):
        self.trayIcon = TrayIcon(self)
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

    def createAct_clicked(self):
        if not self.auth_cert:
            BoxPop.info(self, '此账号尚未完成进阶认证,请前往会员中心完成后【重新登录】!')
            return
        text, ok = BoxPop.input_dialog(self, '新建账号', '请输入账号昵称')
        if not ok or not text:
            return

        def __task():
            try:
                return QsClient.get_instance().add_account(text)
            except Exception as e:
                logging.error(f"添加账号异常:\n{str(e)}")
            return False, "添加账号异常!"

        def __result(args: Tuple[bool, str] = None):
            if not args:
                args = (False, "未知错误!")
            status, msg = args
            if status:
                BoxPop.info(self, msg)
                self.get_account_info()
            else:
                BoxPop.err(self, msg)

        CustomThread.run_task(__task, __result, LoadingMask(self))

    def autoInput_stateChanged(self):
        Config.auto_input(self.checkBox_autoInput.isChecked())

    def dynamicPwd_clicked(self):
        def __task():
            self.get_dynamic_password()
            if not self.nowAccount.dynamic_pwd:
                BoxPop.err(self, f'获取动态密令失败')
                return False
            return True

        def __result(status: bool):
            try:
                if not status:
                    return
                # 需要运行游戏才能执行自动输入
                if self.checkBox_autoInput.isChecked() and SystemCom.check_game_running():
                    status, msg = SystemCom.auto_input_act_pwd(self.nowAccount.id, self.nowAccount.dynamic_pwd)
                    if status != 0:
                        BoxPop.err(self, msg)
            except Exception as e:
                logging.error(f"发生错误:\n{str(e)}")
                BoxPop.err(self, '自动输入失败,请手动复制输入!')

        CustomThread.run_task(__task, __result, LoadingMask(self))

    def start_clicked(self):
        def __task():
            if Config.pass_input():
                self.get_dynamic_password()
                if not self.nowAccount.dynamic_pwd:
                    BoxPop.err(self, f'请求动态密令失败')
                    return False
            return True

        def __result(status: bool):
            try:
                if not status:
                    return
                SystemCom.run_game(self.nowAccount.id, self.nowAccount.dynamic_pwd, self.run_game_result)
            except Exception as e:
                logging.error(f"发生错误:\n{str(e)}")
                BoxPop.err(self, f'启动游戏出现了问题:\n {str(e)}')

        CustomThread.run_task(__task, __result, LoadingMask(self))

    def get_dynamic_password(self):
        try:
            pwd = QsClient.get_instance().get_dynamic_password(self.nowAccount, GLOBAL_CONFIG.bf_web_token)
            pwd = pwd if pwd else None
            self.nowAccount.dynamic_pwd = pwd
            self.lineEdit_dynamicPwd.setText(BaseTools.hidden_str(pwd))
        except Exception as e:
            logging.error(f"发生错误:\n{str(e)}")

    def run_game_result(self, data):
        status, msg = data
        # -999 = 系统异常
        # -1  = 免输入模式错误
        # 0 = 游戏正在运行,不执行
        # 1  = 设置游戏目录
        # 2 = 自动阻止更新成功
        if status == 1:
            if not BoxPop.question(self, msg):
                return
            options = QFileDialog.Options()
            directory = QFileDialog.getExistingDirectory(None, "请选择新枫之谷游戏目录", "", options=options)
            if not directory:
                return
            Config.game_path(directory)
            # 重新打开
            self.start_clicked()
        elif status == 0:
            # 游戏正在运行
            if BoxPop.question(self, '检测到游戏运行中,是否强制结束后重新启动游戏?'):
                SystemCom.kill_mapleStory()
                self.start_clicked()
        elif status == 2:
            logging.info(msg)
            BoxPop.info(self, msg)
        else:
            logging.error(msg)
            BoxPop.warn(self, msg)

    def get_account_info(self, event=None):
        def __task():
            try:
                return QsClient.get_instance().get_account_list(GLOBAL_CONFIG.bf_web_token)
            except Exception as e:
                logging.error(f"发生错误:\n{str(e)}")
            return None

        def __result(actInfoResult: ActInfoResult = None):
            if not actInfoResult:
                BoxPop.err(self, '获取账号信息失败!')
                return
            self.children_accounts = actInfoResult.accounts
            self.auth_cert = actInfoResult.auth_cert
            self.comboBox_gameAct.clear()
            self.pushButton_createAct.setVisible(actInfoResult.new_user)
            self.pushButton_dynamicPwd.setEnabled(not actInfoResult.new_user)
            self.lineEdit_numAct.setText('')
            self.lineEdit_dynamicPwd.setText('')
            if actInfoResult.new_user is True or len(self.children_accounts) == 0:
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

        CustomThread.run_task(__task, __result, LoadingMask(self))

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
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        else:
            self.label_status.setText('封禁')
            palette.setColor(QPalette.WindowText, QColor(255, 0, 0))
        self.label_status.setPalette(palette)
        self.lineEdit_numAct.setText(BaseTools.hidden_str(self.nowAccount.id))
        self.lineEdit_dynamicPwd.setText('')
        self.refresh_points()

    def config_clicked(self):
        GLOBAL_CONFIG.win_config = ConfigWin(self)
        GLOBAL_CONFIG.win_config.exec_()

    def refresh_points(self, event=None):
        def __task():
            try:
                points = QsClient.get_instance().get_game_points(GLOBAL_CONFIG.bf_web_token)
                points_game = math.floor(Decimal(points) / Decimal('2.5'))
                return f"{points}[{points_game}]"
            except Exception as e:
                logging.error(f"发生错误:\n{str(e)}")
            return None

        def __result(template: str = None):
            if not template:
                template = ""
            self.label_points.setText(template)

        CustomThread.run_task(__task, __result, LoadingMask(self))

    def user_loginOut_triggerd(self):
        from src.window.LoginWin import LoginWin
        QsClient.get_instance().login_out()
        win_login = LoginWin()
        win_login.show()
        self.close()
