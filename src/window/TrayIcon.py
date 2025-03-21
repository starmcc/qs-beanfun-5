import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget


class TrayIcon(QSystemTrayIcon):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # 创建菜单和动作
        self.menu = QMenu()
        self.create_menu_actions()

        # 设置图标
        self.set_icon()

        # 连接图标激活信号（点击图标）
        self.activated.connect(self.icon_clicked)

        self.show()

    def create_menu_actions(self):
        """ 创建动作 """
        self.quit_action = QAction("退出", self, triggered=self.quit)
        self.menu.addAction(self.quit_action)
        """ 设置上下文菜单 """
        self.setContextMenu(self.menu)

    def set_icon(self):
        """ 设置图标 """
        self.setIcon(QIcon(':/images/logo'))

    def icon_clicked(self, reason):
        """ 处理图标点击事件 """
        if reason == 2 or reason == 3:
            if self.parent().isVisible():
                self.parent().showMinimized()
                self.parent().hide()
            else:
                self.parent().show()
                self.parent().showNormal()

    def quit(self):
        """ 退出程序 """
        self.setVisible(False)
        QApplication.quit()
        sys.exit()
