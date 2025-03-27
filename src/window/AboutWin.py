import webbrowser

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from src.config.GlobalConfig import GLOBAL_APP_VERSION, GLOBAL_APP_GITHUB
from src.utils import BaseTools, BoxPop
from src.views.Ui_About import Ui_About


class AboutWin(QDialog, Ui_About):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        BaseTools.set_basic_window(self)
        self.init_ui()

    def init_ui(self):
        self.label_version.setText(GLOBAL_APP_VERSION)
        self.label_image.setPixmap(QPixmap(":/images/sponsor"))
        self.label_qq.mousePressEvent = self.qq_mousePressEvent
        self.label_version.mousePressEvent = self.version_mousePressEvent

    def qq_mousePressEvent(self, event):
        webbrowser.open('https://tool.gljlw.com/qq/?qq=1140526018')

    def version_mousePressEvent(self, event):
        BaseTools.check_version(self)