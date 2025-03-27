import logging
import re
import time

import httpx
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QButtonGroup
from PyQt5 import QtWidgets

from src.client import QsClient
from src.config import Config
from src.config.GlobalConfig import *
from src.models.LoginRecord import LoginRecord
from src.utils import BaseTools, BoxPop
from src.utils.ThreadTools import CustomThread
from src.views.Ui_Login import Ui_Login
from src.window import PyQtBrowser
from src.window.ActManagerWin import ActManagerWin
from src.window.IntermediateLoginWin import IntermediateLoginWin
from src.window.LoadMask import LoadMask
from src.window.MainWin import MainWin
from src.window.QrCodeLoginWin import QrCodeLoginWin
from src.window.TwAdvWin import TwAdvWin


class LoginWin(QWidget, Ui_Login):
    login_go_to_main_event = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttonGroup_type = QButtonGroup()
        self.setupUi(self)
        BaseTools.set_basic_window(self)
        self.init_ui()
        self.show()

    def init_ui(self):
        # 设置图片
        self.label_logoView.setPixmap(QPixmap(":/images/banner"))
        self.label_qrCode.setPixmap(QPixmap(":/images/qrCode"))

        self.pushButton_login.clicked.connect(self.login_clicked)
        self.pushButton_actManager.clicked.connect(self.actManager_clicked)
        self.label_register.mousePressEvent = self.register_mousePressEvent
        self.label_forgotPassword.mousePressEvent = self.forgotPassword_mousePressEvent
        self.lineEdit_password.returnPressed.connect(self.login_clicked)
        self.checkBox_remember.stateChanged.connect(self.remember_stateChanged)
        self.label_qrCode.mousePressEvent = self.open_qr_code_win
        # 创建QButtonGroup对象
        self.buttonGroup_type.addButton(self.radioButton_tw)
        self.buttonGroup_type.addButton(self.radioButton_hk)
        self.buttonGroup_type.buttonClicked.connect(self.buttonGroup_type_clicked)

        self.init_account_info()
        self.checkBox_remember.setChecked(Config.remember())

        self.login_go_to_main_event.connect(self.login_go_to_main_win)
        # 初始状态为隐藏密码
        self.is_password_visible = False
        # 创建显示密码动作按钮
        self.show_password_action = QtWidgets.QAction(self)
        # 获取系统自带的可见图标，这里以开启眼睛图标作示例，不同系统显示效果可能有差异
        self.show_password_action.setIcon(QIcon(':/images/pwd_open'))

        def toggle_password_visibility():
            if self.is_password_visible:
                # 如果密码当前可见，将其设为隐藏状态
                self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
                self.show_password_action.setIcon(QIcon(':/images/pwd_open'))
                self.is_password_visible = False
            else:
                # 如果密码当前隐藏，将其设为可见状态
                self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Normal)
                self.show_password_action.setIcon(QIcon(':/images/pwd_close'))
                self.is_password_visible = True

        self.show_password_action.triggered.connect(toggle_password_visibility)
        # 将动作添加到密码输入框
        self.lineEdit_password.addAction(self.show_password_action, QtWidgets.QLineEdit.TrailingPosition)

    def open_qr_code_win(self, event=None):
        GLOBAL_CONFIG.win_qrCode = QrCodeLoginWin(self)
        GLOBAL_CONFIG.win_qrCode.login_win_event.connect(self.login_go_to_main_win)
        GLOBAL_CONFIG.win_qrCode.exec_()

    def buttonGroup_type_clicked(self):
        isTw = self.buttonGroup_type.checkedButton() == self.radioButton_tw
        self.label_qrCode.setVisible(isTw)
        if isTw:
            GLOBAL_CONFIG.now_login_type = GLOBAL_ACT_TYPE_TW
        else:
            GLOBAL_CONFIG.now_login_type = GLOBAL_ACT_TYPE_HK

    def init_account_info(self):
        account = Config.account_first()
        self.lineEdit_account.setText(account.get('account'))
        self.lineEdit_password.setText(account.get('password'))
        type = account.get('login_type') if account.get('login_type') else 'HK'
        if type == 'HK':
            self.radioButton_hk.click()
        elif type == 'TW':
            self.radioButton_tw.click()

    def login_clicked(self):
        CustomThread.run_task(self.task_login, self.task_login_result, LoadMask(self))

    def task_login(self):
        try:
            act = self.lineEdit_account.text()
            pwd = self.lineEdit_password.text()
            return QsClient.get_instance().login(act, pwd)
        except httpx.RequestError as e:
            logging.error(e)
            return LoginRecord(status=False, message='网络错误')

    def task_login_result(self, login_record):
        if login_record.daul_status:
            # 双重验证
            code = self._login_double_input()
            if not code:
                return
            login_record.dual_code = code
            login_record = QsClient.get_instance().dual_very_login(login_record)
        if not login_record.status:
            if login_record.message:
                BoxPop.err(self, login_record.message)
            if login_record.daul_status:
                # 如果是双重验证，但验证码错误，则递归继续执行
                self.task_login_result(login_record)
            return

        if login_record.daul_status:
            # 如果是双重验证，但验证码错误，则递归继续执行
            self.task_login_result(login_record)
            return

        if login_record.adv_status:
            # 台号进阶验证 需要显示图形验证码并填写手机号
            GLOBAL_CONFIG.win_twAdv = TwAdvWin(self)
            GLOBAL_CONFIG.win_twAdv.exec_()
            return

        if login_record.intermediate_login:
            # 台号中級驗證
            GLOBAL_CONFIG.win_intermediateLogin = IntermediateLoginWin(self, login_record)
            GLOBAL_CONFIG.win_intermediateLogin.data_sent.connect(self.task_login_result)
            GLOBAL_CONFIG.win_intermediateLogin.exec_()
            return

        # 登录成功后保存数据
        GLOBAL_CONFIG.bf_web_token = login_record.bfWebToken
        account = self.lineEdit_account.text()
        entry = Config.account_get(account)
        insert = False if entry else True
        entry['account'] = account
        if self.checkBox_remember.isChecked():
            entry['password'] = self.lineEdit_password.text()
        else:
            entry['password'] = ''
        entry['login_type'] = 'HK' if self.buttonGroup_type.checkedButton() == self.radioButton_hk else 'TW'
        entry['last_login_time'] = time.time()

        Config.account_changes(entry, insert)

        self.login_go_to_main_event.emit()

    def _login_double_input(self) -> str:
        text, ok = BoxPop.input_dialog(self, '双重验证', '请填写验证码')
        if ok:
            if re.match(r'^\d+$', text):
                return text
            else:
                return self._login_double_input()
        return ''

    def register_mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            url = QsClient.get_instance().get_web_url_register()
            PyQtBrowser.open_browser(url, self)

    def forgotPassword_mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            url = QsClient.get_instance().get_web_url_forgot_pwd()
            PyQtBrowser.open_browser(url, self)

    def actManager_clicked(self):
        GLOBAL_CONFIG.win_actManager = ActManagerWin(self)
        GLOBAL_CONFIG.win_actManager.exec_()
        self.init_account_info()

    def remember_stateChanged(self):
        Config.remember(self.checkBox_remember.isChecked())

    def login_go_to_main_win(self):
        self.close()

        GLOBAL_CONFIG.win_main = MainWin()
        GLOBAL_CONFIG.win_main.show()
