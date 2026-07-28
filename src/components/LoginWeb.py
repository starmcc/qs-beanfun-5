from PySide6.QtCore import QUrl
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QVBoxLayout, QProgressBar

from src.config.GlobalConfig import GLOBAL_CONFIG, ActType
from src.utils import WinManager
from src.components.BaseWebEngine import BaseWebEngineView

# GamaPass 自动点击 JS
GAMAPASS_AUTO_CLICK_JS = r"""
(function() {
    'use strict';
    var clicked = false;
    function tryClick() {
        if (clicked) return true;
        var btn = document.querySelector('a.use-gama-pass');
        if (btn) {
            btn.click();
            clicked = true;
            console.log('[GamaPass] clicked use-gama-pass');
            return true;
        }
        return false;
    }
    if (!tryClick()) {
        var obs = new MutationObserver(function() {
            if (tryClick()) obs.disconnect();
        });
        if (document.body) {
            obs.observe(document.body, { childList: true, subtree: true });
        }
        var attempts = 0;
        var poller = setInterval(function() {
            attempts++;
            if (tryClick() || attempts > 50) {
                clearInterval(poller);
                obs.disconnect();
            }
        }, 200);
    }
})();
"""


class LoginWeb(QDialog):
    """内置浏览器登录窗口（单例）。检测到 bfWebToken 后自动完成登录。"""

    _instance = None

    def __init__(self, parent, is_gamapass=False):
        if LoginWeb._instance is not None:
            raise Exception("LoginWeb 窗口只能打开一个")
        super().__init__(parent)
        LoginWeb._instance = self
        self._is_gamapass = is_gamapass
        self._auto_login_done = False
        GLOBAL_CONFIG.bf_web_token = None
        self._setup_window()
        self._init_ui()
        self._connect_signals()

    def _setup_window(self):
        WinManager.set_basic_window(self)
        self.setMinimumSize(1024, 800)
        if self._is_gamapass:
            self.setWindowTitle(WinManager.translate("台湾游戏橘子 - GamaPass 登入"))
        else:
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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.web_view, 1)

    def _connect_signals(self):
        self.web_view.loadStarted.connect(self._on_load_started)
        self.web_view.loadProgress.connect(self._on_load_progress)
        self.web_view.loadFinished.connect(self._on_load_finished)
        self.web_view.bf_token_ready.connect(self._on_token_ready)

    def _on_load_started(self):
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def _on_load_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress >= 100:
            self.progress_bar.hide()

    def _on_load_finished(self, status):
        self.progress_bar.hide()
        if self._is_gamapass and status:
            current_url = self.web_view.url().toString()
            if 'Login/Index' in current_url or 'bflogin/default.aspx' in current_url:
                self.web_view.page().runJavaScript(GAMAPASS_AUTO_CLICK_JS)

    def _on_token_ready(self):
        """bfWebToken 捕获后自动完成登录"""
        if self._auto_login_done:
            return
        self._auto_login_done = True
        self.web_view.sync_cookies_to_requests()
        self.parent().login_go_to_main_event.emit()
        self.close()

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


def open_login_page(url_path: str, parent, is_gamapass=False):
    """打开登录页面（单例复用）"""
    if LoginWeb._instance is not None:
        LoginWeb._instance.showNormal()
        LoginWeb._instance.raise_()
        return LoginWeb._instance
    win = LoginWeb(parent, is_gamapass=is_gamapass)
    win.load_url(url_path)
    win.show()
    return win
