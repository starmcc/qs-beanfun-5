import webbrowser

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog

from src.config.GlobalConfig import GlobalConstants
from src.utils import BaseTools, WinManager
from src.views.Ui_About import Ui_About


class AboutWin(QDialog, Ui_About):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        WinManager.set_basic_window(self)
        self.init_ui()

    def init_ui(self):
        self.label_version.setText(GlobalConstants.APP_VERSION)
        self.label_image.setPixmap(QPixmap(":/images/sponsor"))
        self.label_qq.mousePressEvent = self.qq_mousePressEvent
        self.label_version.mousePressEvent = self.version_mousePressEvent

    def qq_mousePressEvent(self, event):
        webbrowser.open('https://tool.gljlw.com/qq/?qq=1140526018')

    def version_mousePressEvent(self, event):
        BaseTools.check_new_version(self, False)