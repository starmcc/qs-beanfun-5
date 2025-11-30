from PyQt5.QtWidgets import QDialog

from src.config import Config
from src.utils import WinManager, BoxPop, SystemCom
from src.views.Ui_Config import Ui_Config
from src.window import CustomToolTipWin


class ConfigWin(QDialog, Ui_Config):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        WinManager.set_basic_window(self)
        self.init_ui()
        self.read_config()

    def init_ui(self):
        self.checkBox_passInput.stateChanged.connect(self.passInput_statusChanged)
        CustomToolTipWin.build_tips(self, self.checkBox_passInput, "启动游戏将直接跳过登录界面\n与网页登录相似\n不建议开启该功能")
        self.checkBox_stopUpdate.stateChanged.connect(self.stopUpdate_statusChanged)
        CustomToolTipWin.build_tips(self, self.checkBox_stopUpdate, "由于连接台服可能存在网络波动导致更新失败\n一般情况下请默认勾选阻止游戏自动更新\n建议通过官网下载最新补丁手动更新")
        self.checkBox_closeStartWindow.stateChanged.connect(self.closeStartWindow_statusChanged)
        CustomToolTipWin.build_tips(self, self.checkBox_closeStartWindow, "《新枫之谷》启动后,会打开默认启动页\n建议勾选自动关闭该启动页\n该启动页无任何作用,加快游戏启动速度")
        self.pushButton_gamePath.clicked.connect(self.gamePath_clicked)
        CustomToolTipWin.build_tips(self, self.pushButton_gamePath, "选择游戏目录\n请选择英文目录")


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
        directory, err = SystemCom.select_game_path()
        if not directory:
            return
        if err:
            BoxPop.warn(self, err)
            return
        self.lineEdit_gamePath.setText(Config.game_path())