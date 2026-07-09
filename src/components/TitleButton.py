import logging

from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QPixmap, Qt, QIcon
from PySide6.QtWidgets import QMenu, QPushButton

from src.config.StyleConstants import StyleConstants


class TitleButton(QPushButton):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.init_ui()

    def init_ui(self):
        self.setText("")
        self.setFixedSize(28, 28)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMouseTracking(True)
        self.load_icon()
        self.setStyleSheet(StyleConstants.TITLE_BTN)

    def load_icon(self):
        pixmap = QPixmap(self.icon_path)
        if pixmap.isNull():
            logging.error(f"警告：无法加载图标 {self.icon_path}")
            self.setText("?")
            return
        scaled_pixmap = pixmap.scaled(
            16, 16,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setIcon(QIcon(scaled_pixmap))
        self.setIconSize(QSize(16, 16))

    def set_menu(self, menu: QMenu):
        self.menu = menu
        self.menu.aboutToHide.connect(self.reset_state)
        self.clicked.connect(self.show_menu)

    def show_menu(self):
        if self.menu:
            self.menu.exec(self.mapToGlobal(self.rect().bottomLeft()))

    @Slot()
    def reset_state(self):
        self.update()
