import logging
from datetime import datetime

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QDialog

from src.client import QsClient
from src.models.Account import Account
from src.utils import BaseTools, BoxPop
from src.views.Ui_AccountInfo import Ui_AccountInfo


class AccountInfoWin(QDialog, Ui_AccountInfo):
    notice_refresh = pyqtSignal()

    def __init__(self, parent=None, account: Account = None):
        super().__init__(parent)
        self.account: Account = account
        BaseTools.set_basic_window(self)
        self.setupUi(self)
        self.init_ui()
        self.init_data()

    def init_ui(self):
        self.pushButton_edit.clicked.connect(self.edit_account)

    def init_data(self):
        self.label_account.setText(self.account.id)
        self.label_name.setText(self.account.name)
        self.label_number.setText(self.account.sn)
        palette = self.label_status.palette()
        if self.account.status:
            self.label_status.setText('正常')
            palette.setColor(QPalette.WindowText, QColor(0, 0, 255))
        else:
            self.label_status.setText('禁止')
            palette.setColor(QPalette.WindowText, QColor(255, 0, 0))
        self.label_status.setPalette(palette)
        date = datetime.strptime(self.account.create_time, "%Y-%m-%d %H:%M:%S")
        day = abs(date - datetime.now()).days
        self.label_day.setText(f'{day}')
        self.label_createTme.setText(f"于 {self.account.create_time} 创建")


    def edit_account(self):
        text, ok = BoxPop.input_dialog(self, '修改賬戶名稱', '請輸入新的賬戶名稱')
        if not ok or not text:
            return
        try:
            status, msg = QsClient.get_instance().change_account_name(self.account.id, text)
            if not status:
                BoxPop.err(self, msg)
                return
            else:
                BoxPop.info(self, msg)
            self.notice_refresh.emit()
            self.close()
        except Exception as e:
            logging.error(e)
            BoxPop.info(self, '操作異常！')
