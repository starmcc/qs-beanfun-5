from PySide6.QtCore import QUrl
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton

from src.config.GlobalConfig import GLOBAL_CONFIG, ActType
from src.utils import WinManager, BoxPop
from src.window.BaseWebEngine import BaseWebEngineView


class LoginWeb(QDialog):
    """内置浏览器登录窗口（单例）。使用 BaseWebEngineView，每次打开都是全新会话。"""

    _instance = None

    def __init__(self, parent):
        if LoginWeb._instance is not None:
            raise Exception("LoginWeb 窗口只能打开一个")
        super().__init__(parent)
        LoginWeb._instance = self
        GLOBAL_CONFIG.bf_web_token = None
        self._setup_window()
        self._init_ui()
        self._connect_signals()

    def _setup_window(self):
        WinManager.set_basic_window(self)
        self.setMinimumSize(1024, 800)
        type_act = "香港" if GLOBAL_CONFIG.now_login_type != ActType.TW.value else "台湾"
        self.setWindowTitle(WinManager.translate(f"{type_act}游戏橘子 - 登入"))

    def _init_ui(self):
        self.web_view = BaseWebEngineView(self)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet("""
            QProgressBar { background-color: #E5E6EB; border: none; border-radius: 1px; }
            QProgressBar::chunk { background-color: #165DFF; border-radius: 1px; }
        """)
        self.progress_bar.hide()

        self.enter_btn = QPushButton(WinManager.translate("确认登入状态(请成功登入后点击此处)"))
        self.enter_btn.setFixedHeight(38)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.web_view, 1)
        layout.addWidget(self.enter_btn)

    def _connect_signals(self):
        self.web_view.loadStarted.connect(self._on_load_started)
        self.web_view.loadProgress.connect(self._on_load_progress)
        self.web_view.loadFinished.connect(self._on_load_finished)
        self.enter_btn.clicked.connect(self._on_login_enter)

    def _on_load_started(self):
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def _on_load_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress >= 100:
            self.progress_bar.hide()

    def _on_load_finished(self, status):
        self.progress_bar.hide()

    def _on_login_enter(self):
        if GLOBAL_CONFIG.bf_web_token:
            self.web_view.sync_cookies_to_requests()
            self.parent().login_go_to_main_event.emit()
            self.close()
        else:
            BoxPop.info(self, "請先在網頁進行登入\n登入成功後再點此處完成登入")

    def load_url(self, url: str):
        if url.startswith(("http://", "https://")):
            self.web_view.load(QUrl(url))
        else:
            self.web_view.load(QUrl(f"https://{url}"))

    def closeEvent(self, event: QCloseEvent):
        if hasattr(self, "web_view"):
            self.web_view.stop()
            self.web_view.load(QUrl("about:blank"))
            self.web_view.deleteLater()
        LoginWeb._instance = None
        event.accept()


def open_login_page(url_path: str, parent):
    """打开登录页面（单例复用）"""
    if LoginWeb._instance is not None:
        LoginWeb._instance.showNormal()
        LoginWeb._instance.raise_()
        return LoginWeb._instance
    win = LoginWeb(parent)
    win.load_url(url_path)
    win.show()
    return win
