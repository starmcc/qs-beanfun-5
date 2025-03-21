from PyQt5.QtWidgets import QFileDialog, QDialog

from src.config import Config
from src.utils import BaseTools
from src.views.Ui_Config import Ui_Config


class ConfigWin(QDialog, Ui_Config):
    def __init__(self, parent=None):
        super().__init__(parent)
        BaseTools.set_basic_window(self)
        self.setupUi(self)
        self.init_ui()
        self.read_config()

    def init_ui(self):
        self.checkBox_passInput.stateChanged.connect(self.passInput_statusChanged)
        self.checkBox_stopUpdate.stateChanged.connect(self.stopUpdate_statusChanged)
        self.checkBox_closeStartWindow.stateChanged.connect(self.closeStartWindow_statusChanged)
        self.pushButton_gamePath.clicked.connect(self.gamePath_clicked)

    def read_config(self):
        self.checkBox_passInput.setChecked(Config.pass_input())
        self.checkBox_stopUpdate.setChecked(Config.stop_update())
        self.checkBox_closeStartWindow.setChecked(Config.close_start_window())
        self.lineEdit_gamePath.setText(Config.game_path())

    def passInput_statusChanged(self):
        Config.pass_input(self.checkBox_passInput.isChecked())

    def stopUpdate_statusChanged(self):
        Config.stop_update(self.checkBox_stopUpdate.isChecked())

    def closeStartWindow_statusChanged(self):
        Config.close_start_window(self.checkBox_closeStartWindow.isChecked())

    def gamePath_clicked(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(None, "选择新枫之谷游戏目录", "", options=options)
        if not directory:
            return
        self.lineEdit_gamePath.setText(directory)
        Config.game_path(directory)
