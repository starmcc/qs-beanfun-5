import locale
import logging
import os
import sys
import webbrowser
import zipfile

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from packaging import version

from src import zhconv
from src.client import RequestClient
from src.config import GlobalConfig
from src.config.GlobalConfig import GLOBAL_APP_VERSION, GLOBAL_APP_GITHUB_API, GLOBAL_APP_GITHUB
from src.utils import BoxPop


def hidden_str(s):
    if s and len(s) > 5:
        return s[:5] + '*' * (len(s) - 5)
    else:
        return s


def build_path(path: str, env: bool = False):
    if not env and getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        p = os.path.dirname(sys.executable)
        return rf'{p}\{path}'
    # 如果是在开发环境中运行
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    return rf'{p}\{path}'


def set_basic_window(self: QWidget):
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QIcon
    from src.window.LoginWin import LoginWin
    from src.window.MainWin import MainWin
    from src.window.AboutWin import AboutWin
    from src.window.AccountInfoWin import AccountInfoWin
    from src.window.ConfigWin import ConfigWin
    from src.window.PyQtBrowser import _PyQtBrowser
    from src.window.ActManagerWin import ActEditWin, ActManagerWin
    from src.window.TwAdvWin import TwAdvWin
    from src.window.QrCodeLoginWin import QrCodeLoginWin
    from src.window.IntermediateLoginWin import IntermediateLoginWin
    self.setWindowIcon(QIcon(":/images/logo"))
    # 所有窗口透明度
    self.setWindowOpacity(0.97)
    self.setStyleSheet("""
    * {
    font-family: '微软雅黑';
    }
    
    QLineEdit {
    border: 1px solid #a0a0a0;  /* 边框宽度为 1px，颜色为 #a0a0a0 */
    border-radius: 3px;  /* 边框圆角 */
    padding-left: 5px;  /* 文本距离左边界有 5px */
    background-color: transparent;  /* 背景颜色 */
    color: black;  /* 文本颜色 */
    selection-background-color: #F57C00;  /* 选中文本的背景颜色 */
    font-size: 10pt;  /* 文本字体大小 */
    }
    
    QLineEdit:hover {  /* 鼠标悬浮在 QLineEdit 时的状态 */
        border: 1px solid #F57C00;
        border-radius: 3px;
        background-color: #f2f2f2;
        color: #F57C00;
        selection-background-color: #F57C00;
    }
    
    
    QLineEdit[echoMode="2"] {  /* QLineEdit 有输入掩码时的状态 */
        lineedit-password-character: 9679;
    }
    """)

    # 将所有空间转成对应语言
    translate_all_controls(self)

    if (isinstance(self, ConfigWin)
            or isinstance(self, AccountInfoWin)
            or isinstance(self, AboutWin)
            or isinstance(self, ActEditWin)
            or isinstance(self, ActManagerWin)
            or isinstance(self, TwAdvWin)
            or isinstance(self, QrCodeLoginWin)
            or isinstance(self, IntermediateLoginWin)):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    elif isinstance(self, LoginWin):
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle(f'{self.windowTitle()} {GLOBAL_APP_VERSION}')
    elif isinstance(self, MainWin):
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle(f'{self.windowTitle()} {GLOBAL_APP_VERSION}')
    elif isinstance(self, _PyQtBrowser):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.WindowMaximizeButtonHint)


def extract_build_plugin(plugin_name):
    # 从 ZIP 文件路径中获取文件名（不包含扩展名）作为目标文件夹名
    plugin_directory = build_path(rf'plugins\{os.path.splitext(plugin_name)[0]}')
    # 确保目标目录存在，如果不存在则创建
    if os.path.exists(plugin_directory):
        return plugin_directory
    else:
        os.makedirs(plugin_directory)

    zip_file_path = build_path(rf'resources\plugins\{plugin_name}', True)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(plugin_directory)

    return plugin_directory


def check_version(self):
    try:
        response = RequestClient.get_instance().get(f"{GLOBAL_APP_GITHUB_API}/releases/latest")
        response.raise_for_status()
        data = response.json()
        latest_version = data.get('tag_name')
        if latest_version is None:
            BoxPop.err(self, "無法獲取版本信息")
            return
        try:
            if version.parse(GlobalConfig.GLOBAL_APP_VERSION) >= version.parse(latest_version):
                BoxPop.info(self, "當前已是最新版本")
            elif BoxPop.question(self, f"發現新版本 {latest_version}，是否前往更新？"):
                webbrowser.open(f'{GLOBAL_APP_GITHUB}/releases')
        except version.InvalidVersion as e:
            logging.error(f"解析版本失敗{e}")
            BoxPop.err(self, "解析版本失敗")
    except ValueError as e:
        logging.error(f"解析 JSON 出错: {e}")
        BoxPop.err(self, "解析版本失敗2")


def translate_all_controls(self):
    # 定义需要转换文本的控件类型
    control_types = (QtWidgets.QLabel, QtWidgets.QPushButton, QtWidgets.QCheckBox,
                     QtWidgets.QRadioButton, QtWidgets.QGroupBox, QtWidgets.QComboBox,
                     QtWidgets.QAction, QtWidgets.QMenu)
    # 查找所有指定类型的控件
    widgets = self.findChildren(control_types)
    for widget in widgets:
        if hasattr(widget, 'text') and callable(widget.text):
            # 进行简转繁
            text = translate(widget.text())
            if hasattr(widget, 'setText') and callable(widget.setText):
                widget.setText(text)
            elif isinstance(widget, QtWidgets.QMenu):
                widget.setTitle(text)
    # 转换窗口标题
    self.setWindowTitle(translate(self.windowTitle()))


def translate(text):
    return zhconv.convert(text, 'zh-cn' if is_windows_simplified_chinese() else 'zh-tw')


def is_windows_simplified_chinese():
    try:
        # 获取系统默认语言环境
        lang, _ = locale.getdefaultlocale()
        simplified_codes = {
            "zh_CN", "zh-CN",
            "zh_Hans_CN",
            "zh_SG", "zh-SG",
            "zh_Hans_SG"
        }
        return lang in simplified_codes
    except Exception as e:
        print(f"获取系统语言时出现异常: {e}")
        return False
