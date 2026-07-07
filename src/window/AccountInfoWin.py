import logging
from datetime import datetime

from PySide6.QtCore import pyqtSignal
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QDialog

from src.client import QsClient
from src.models.Account import Account
from src.utils import BoxPop, WinManager
from src.views.Ui_AccountInfo import Ui_AccountInfo


class AccountInfoWin(QDialog, Ui_AccountInfo):
    notice_refresh = pyqtSignal()

    def __init__(self, parent=None, account: Account = None):
        super().__init__(parent)
        self.account: Account = account
        self.setupUi(self)
        WinManager.set_basic_window(self)
        self.init_ui(parent)
        self.init_data()

    def init_ui(self, parent):
        self.pushButton_edit.clicked.connect(self.edit_account)
        self.notice_refresh.connect(parent.get_account_info)

    def init_data(self):
        self.label_account.setText(self.account.id)
        self.label_name.setText(self.account.name)
        self.label_number.setText(self.account.sn)
        palette = self.label_status.palette()
        if self.account.status:
            self.label_status.setText('正常')
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 255))
        else:
            self.label_status.setText('禁止')
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 0, 0))
        self.label_status.setPalette(palette)
        try:
            date = datetime.strptime(self.account.create_time, "%Y-%m-%d %H:%M:%S")
            day = abs(date - datetime.now()).days
            self.label_day.setText(f'{day}')
        except Exception as e:
            logging.error(f"发生错误:\n{str(e)}")
        self.label_createTme.setText(f"于 {self.account.create_time} 创建")

    def edit_account(self):
        text, ok = BoxPop.input_dialog(self, '修改账号名称', '请输入新的账号名称')
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
            logging.error(f"发生错误:\n{str(e)}")
            BoxPop.info(self, '操作异常！')