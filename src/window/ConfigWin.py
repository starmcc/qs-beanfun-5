from PySide6.QtWidgets import QDialog

from src.config import Config, GlobalConfig
from src.config.I18n import I18N
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
        self._language_values = (GlobalConfig.LANGUAGE.ZH_CN.value, GlobalConfig.LANGUAGE.ZH_TW.value,
                                 GlobalConfig.LANGUAGE.EN.value)
        self.comboBox_language.currentIndexChanged.connect(self.language_changed)
        I18N.language_changed.connect(lambda _language: self._refresh_language_items())
        self._refresh_language_items()
        self.checkBox_passInput.stateChanged.connect(self.passInput_statusChanged)
        CustomToolTipWin.build_tips(self, self.checkBox_passInput,
                                    "启动游戏将直接跳过登录界面\n与网页登录相似\n不建议开启该功能")
        self.checkBox_stopUpdate.stateChanged.connect(self.stopUpdate_statusChanged)
        CustomToolTipWin.build_tips(self, self.checkBox_stopUpdate,
                                    "由于连接台服可能存在网络波动导致更新失败\n一般情况下请默认勾选阻止游戏自动更新\n建议通过官网下载最新补丁手动更新")
        self.checkBox_appCheckUpdate.stateChanged.connect(self.appCheckUpdate_statusChanged)
        CustomToolTipWin.build_tips(self, self.checkBox_appCheckUpdate, "每次启动工具检查版本更新\n取消勾选则不检查")
        self.checkBox_closeStartWindow.stateChanged.connect(self.closeStartWindow_statusChanged)
        CustomToolTipWin.build_tips(self, self.checkBox_closeStartWindow,
                                    "《新枫之谷》启动后,会打开默认启动页\n建议勾选自动关闭该启动页\n该启动页无任何作用,加快游戏启动速度")
        self.checkBox_ggmFirst.stateChanged.connect(self.ggmFirst_statusChanged)
        CustomToolTipWin.build_tips(self, self.checkBox_ggmFirst,
                                    "使用 GGM（Gamania Games Manager）获取动态密令\n需要本地已安装 GGM 才能生效")
        self.pushButton_gamePath.clicked.connect(self.gamePath_clicked)
        CustomToolTipWin.build_tips(self, self.pushButton_gamePath, "选择游戏目录\n请选择英文目录")

    def _refresh_language_items(self):
        current = I18N.language
        self.comboBox_language.blockSignals(True)
        self.comboBox_language.clear()
        # 语言名称使用各自的原生写法，切换应用语言时保持稳定。
        self.comboBox_language.addItems(["简体中文", "繁體中文", "English"])
        self.comboBox_language.setCurrentIndex(self._language_values.index(current))
        self.comboBox_language.blockSignals(False)

    def language_changed(self, index):
        if 0 <= index < len(self._language_values):
            I18N.set_language(self._language_values[index])
            self._refresh_language_items()

    def read_config(self):
        self.checkBox_passInput.setChecked(Config.pass_input())
        self.checkBox_stopUpdate.setChecked(Config.stop_update())
        self.checkBox_closeStartWindow.setChecked(Config.close_start_window())
        self.checkBox_appCheckUpdate.setChecked(Config.app_check_update())
        self.checkBox_ggmFirst.setChecked(Config.ggm_use())
        self.lineEdit_gamePath.setText(Config.game_path())
        self._refresh_language_items()

    def passInput_statusChanged(self):
        Config.pass_input(self.checkBox_passInput.isChecked())

    def stopUpdate_statusChanged(self):
        Config.stop_update(self.checkBox_stopUpdate.isChecked())

    def closeStartWindow_statusChanged(self):
        Config.close_start_window(self.checkBox_closeStartWindow.isChecked())

    def appCheckUpdate_statusChanged(self):
        Config.app_check_update(self.checkBox_appCheckUpdate.isChecked())

    def ggmFirst_statusChanged(self):
        Config.ggm_use(self.checkBox_ggmFirst.isChecked())

    def gamePath_clicked(self):
        directory, err = SystemCom.select_game_path()
        if not directory:
            return
        if err:
            BoxPop.warn(self, err)
            return
        self.lineEdit_gamePath.setText(Config.game_path())
