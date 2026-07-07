import logging
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget

from src.config.StyleConstants import StyleConstants


def get_win_manager():
    from src.utils import WinManager
    return WinManager


class TrayIcon(QSystemTrayIcon):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # 创建菜单和动作
        self.menu = None
        self.create_menu([{"name": "显示", "func": self.showSelf}])
        """ 设置图标 """
        self.setIcon(QIcon(':/images/logo'))

        self.setToolTip("QsBeanfun\n双击：显示/隐藏窗口\n右键：打开菜单")

        self.activated.connect(self.icon_clicked)
        self.show()

    def create_menu(self, menus: list[dict]):
        self.menu = QMenu()
        self.menu.setStyleSheet(StyleConstants.TRAY_MENU_STYLE)

        if menus:
            for menu in menus:
                action = QAction(menu['name'], self)
                action.triggered.connect(menu['func'])
                self.menu.addAction(action)

        self.menu.addSeparator()

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit)
        self.menu.addAction(quit_action)
        self.setContextMenu(self.menu)

    def icon_clicked(self, reason):
        """ 处理图标点击事件 """
        # Qt6 QSystemTrayIcon.ActivationReason 枚举
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick or reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.parent().isVisible():
                self.parent().showMinimized()
                self.parent().hide()
                self.showMsg("程序已最小化到托盘", "QsBeanfun")
            else:
                self.showSelf()

    def showSelf(self):
        """显示主窗口"""
        if self.parent():
            self.parent().show()
            self.parent().showNormal()
            self.parent().raise_()
            self.parent().activateWindow()

    def showMsg(self, msg, title=""):
        """显示优雅的通知"""
        win_manager = get_win_manager()
        self.showMessage(
            win_manager.translate(title),
            win_manager.translate(msg),
            QIcon(self.create_notification_icon()),
            2000
        )

    def create_notification_icon(self):
        """创建通知图标（带轻微发光效果）"""
        base_pixmap = QPixmap(':/images/logo')
        if base_pixmap.isNull():
            return QIcon(':/images/logo')

        highlighted = QPixmap(base_pixmap.size())
        highlighted.fill(Qt.GlobalColor.transparent)

        painter = QPainter(highlighted)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # 绘制基础图标
        painter.drawPixmap(0, 0, base_pixmap)

        # 添加轻微发光效果
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Overlay)
        painter.fillRect(highlighted.rect(), QColor(255, 255, 255, 30))

        painter.end()
        return highlighted

    def quit(self):
        """优雅退出程序"""
        logging.info("QsBeanfun正在退出")
        self.showMsg("正在安全退出...", "QsBeanfun")

        # 延迟退出确保通知显示
        QTimer.singleShot(500, self._safe_quit)

    def _safe_quit(self):
        """安全退出"""
        try:
            self.setVisible(False)
            if self.menu:
                self.menu.clear()
        except Exception as e:
            logging.error(f"退出时发生错误: {e}")
        finally:
            QApplication.quit()
            sys.exit()
