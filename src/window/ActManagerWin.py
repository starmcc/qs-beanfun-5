from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMenu, QHeaderView, QDialog

from src.config import Config
from src.config.GlobalConfig import GLOBAL_ACT_TYPE_HK, GLOBAL_ACT_TYPE_TW
from src.utils import BaseTools, BoxPop
from src.views.Ui_AccountEdit import Ui_AccountEdit
from src.views.Ui_ActManager import Ui_ActManager


class CustomQTableWidgetItem(QTableWidgetItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextAlignment(Qt.AlignCenter)


class ActEditWin(QDialog, Ui_AccountEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        BaseTools.set_basic_window(self)
        self.setupUi(self)
        self.account = ''
        self.editAct = {}
        self.insert = False
        self.init_ui()

    def init_ui(self):
        self.pushButton_save.clicked.connect(self.save_clicked)

    def init_data(self, account: str = '', insert: bool = False):
        # 查找账号
        self.account = account
        self.insert = insert
        self.editAct = Config.account_get(self.account)
        self.lineEdit_account.setText(self.editAct.get('account'))
        self.lineEdit_password.setText(self.editAct.get('password'))
        self.lineEdit_desc.setText(self.editAct.get('desc'))
        self.lineEdit_account.setEnabled(insert)

        if insert:
            self.lineEdit_account.setFocus()
        else:
            self.lineEdit_password.setFocus()

        if self.editAct.get('login_type') == GLOBAL_ACT_TYPE_TW:
            self.radioButton_tw.setChecked(True)
        else:
            self.radioButton_hk.setChecked(True)

    def save_clicked(self):
        # 判断
        if not self.lineEdit_account.text():
            BoxPop.err(self, '账号不能为空!')
            return
        self.editAct['account'] = self.lineEdit_account.text()
        self.editAct['password'] = self.lineEdit_password.text()
        self.editAct['desc'] = self.lineEdit_desc.text()
        self.editAct['login_type'] = GLOBAL_ACT_TYPE_HK if self.radioButton_hk.isChecked() else GLOBAL_ACT_TYPE_TW
        status, msg = Config.account_changes(self.editAct, self.insert)
        if status:
            BoxPop.info(self, msg)
            self.close()
        else:
            BoxPop.err(self, msg)


class ActManagerWin(QDialog, Ui_ActManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        BaseTools.set_basic_window(self)
        self.setupUi(self)
        self.init_ui()
        self.win_actEdit = ActEditWin(self)

    def init_ui(self):
        # 禁止列移动
        self.tableWidget.horizontalHeader().setSectionsMovable(False)
        # 自适应列宽
        self.tableWidget.setColumnCount(4)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # 双击后应用
        self.tableWidget.doubleClicked.connect(self.tableWidget_doubleClicked)

        # 设置右键菜单
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.show_context_menu)

    def showEvent(self, a0):
        super().showEvent(a0)
        self.accounts_refresh()

    def tableWidget_doubleClicked(self):
        select = self.tableWidget.selectedIndexes()
        item = self.tableWidget.item(select[0].row(), 0)
        Config.account_first(item.text())
        self.close()

    def accounts_refresh(self):
        acts = Config.accounts()
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(acts))
        column_name = ('賬戶', '登入地區', '描述', '最後登入時間')
        self.tableWidget.setHorizontalHeaderLabels(column_name)

        for index, act in enumerate(acts):
            self.tableWidget.setItem(index, 0, CustomQTableWidgetItem(act.get('account')))
            login_type = ''
            if act.get('login_type') == GLOBAL_ACT_TYPE_TW:
                login_type = '台灣'
            else:
                login_type = '香港'
            self.tableWidget.setItem(index, 1, CustomQTableWidgetItem(login_type))
            self.tableWidget.setItem(index, 2, CustomQTableWidgetItem(act.get('desc')))
            if act.get('last_login_time'):
                self.tableWidget.setItem(index, 3, CustomQTableWidgetItem(
                    datetime.fromtimestamp(act.get('last_login_time')).strftime('%Y-%m-%d %H:%M:%S')))

        self.tableWidget.clearSelection()

    def show_context_menu(self, position):
        menu = QMenu()
        refresh_action = menu.addAction("刷新")
        add_action = menu.addAction("增加")
        delete_action = None
        edit_action = None
        selected_indexes = self.tableWidget.selectedIndexes()
        if selected_indexes:
            edit_action = menu.addAction("編輯")
            delete_action = menu.addAction("刪除")

        action = menu.exec_(self.tableWidget.mapToGlobal(position))

        if action == refresh_action:
            self.accounts_refresh()
            return
        elif action == add_action:
            self.win_actEdit.init_data('', True)
            self.win_actEdit.exec_()
            self.accounts_refresh()
            return

        if action == delete_action:
            select = self.tableWidget.selectedIndexes()
            if len(select) > 0:
                item = self.tableWidget.item(select[0].row(), 0)
                if BoxPop.question(self, f'是否刪除賬戶[{item.text()}]?'):
                    Config.account_del(item.text())
        elif action == edit_action:
            select = self.tableWidget.selectedIndexes()
            if len(select) > 0:
                item = self.tableWidget.item(select[0].row(), 0)
                self.win_actEdit.init_data(item.text())
                self.win_actEdit.exec_()
        self.accounts_refresh()
