import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget

from src.utils import WinManager


class TrayIcon(QSystemTrayIcon):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # 创建菜单和动作
        self.menu = None
        self.create_menu([{"name": "显示", "func": self.showSelf}])
        """ 设置图标 """
        self.setIcon(QIcon(':/images/logo'))
        self.activated.connect(self.icon_clicked)
        self.show()

    def create_menu(self, menus: list[dict]):
        self.menu = QMenu()
        if menus:
            for menu in menus:
                action = QAction(menu['name'], self)
                action.triggered.connect(menu['func'])
                self.menu.addAction(action)

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit)
        self.menu.addAction(quit_action)
        self.setContextMenu(self.menu)

    def icon_clicked(self, reason):
        """ 处理图标点击事件 """
        if reason == 2 or reason == 3:
            if self.parent().isVisible():
                self.parent().showMinimized()
                self.parent().hide()
                self.showMsg("程序已最小化到托盘")
            else:
                self.showSelf()

    def showSelf(self):
        self.parent().show()
        self.parent().showNormal()

    def showMsg(self, msg, title=""):
        self.showMessage(WinManager.translate(title), WinManager.translate(msg), self.icon(), 1000)

    def quit(self):
        """ 退出程序 """
        self.setVisible(False)
        QApplication.quit()
        sys.exit()
