from PySide6.QtCore import QUrl
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar

from src.utils import WinManager
from src.window.BaseWebEngine import BaseWebEngineView


class PyQtBrowser(QDialog):
    """通用内置浏览器窗口（单例）。使用 BaseWebEngineView，每次打开都是全新会话。"""

    _instance = None

    def __init__(self, parent=None):
        if PyQtBrowser._instance is not None:
            raise Exception("PyQtBrowser 窗口只能打开一个")
        super().__init__(parent)
        PyQtBrowser._instance = self
        self._setup_window()
        self._init_ui()
        self._connect_signals()

    def _setup_window(self):
        WinManager.set_basic_window(self)
        self.setMinimumSize(880, 550)
        self.setWindowTitle("浏览器")

    def _init_ui(self):
        self.web_view = BaseWebEngineView(self)
        self.url_bar = QLineEdit()
        self.go_btn = QPushButton("进入")
        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.refresh_btn = QPushButton("↻")
        self.progress_bar = QProgressBar()

        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet("""
            QProgressBar { background-color: #E5E6EB; border: none; border-radius: 1px; }
            QProgressBar::chunk { background-color: #165DFF; border-radius: 1px; }
        """)
        self.progress_bar.hide()

        for btn in (self.back_btn, self.forward_btn, self.refresh_btn):
            btn.setMinimumWidth(36)
        self.go_btn.setMinimumWidth(60)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(3)
        top_layout.addWidget(self.back_btn)
        top_layout.addWidget(self.forward_btn)
        top_layout.addWidget(self.refresh_btn)
        top_layout.addWidget(self.url_bar)
        top_layout.addWidget(self.go_btn)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(3, 3, 3, 3)
        main_layout.setSpacing(0)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.web_view, 1)

    def _connect_signals(self):
        self.back_btn.clicked.connect(self.web_view.back)
        self.forward_btn.clicked.connect(self.web_view.forward)
        self.refresh_btn.clicked.connect(self.web_view.reload)
        self.go_btn.clicked.connect(self._load_from_bar)
        self.url_bar.returnPressed.connect(self._load_from_bar)
        self.web_view.loadStarted.connect(self._on_load_started)
        self.web_view.loadProgress.connect(self._on_load_progress)
        self.web_view.loadFinished.connect(self._on_load_finished)
        self.web_view.titleChanged.connect(self.setWindowTitle)

    def _on_load_started(self):
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def _on_load_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress >= 100:
            self.progress_bar.hide()

    def _on_load_finished(self, status):
        self.url_bar.setText(self.web_view.url().url())
        self.progress_bar.hide()

    def _load_from_bar(self):
        url = self.url_bar.text().strip()
        if url:
            self.load_url(url)

    def load_url(self, url: str):
        self.url_bar.setText(url)
        if url.startswith(("http://", "https://")):
            self.web_view.load(QUrl(url))
        else:
            self.web_view.load(QUrl(f"https://{url}"))

    def load_html(self, html: str):
        self.web_view.setHtml(html)

    def closeEvent(self, event: QCloseEvent):
        if hasattr(self, "web_view"):
            self.web_view.stop()
            self.web_view.load(QUrl("about:blank"))
            self.web_view.deleteLater()
        PyQtBrowser._instance = None
        event.accept()


def open_browser(url_path: str, parent=None):
    """打开通用浏览器窗口（单例复用）"""
    if PyQtBrowser._instance is not None:
        PyQtBrowser._instance.showNormal()
        PyQtBrowser._instance.raise_()
        PyQtBrowser._instance.load_url(url_path)
        return PyQtBrowser._instance
    win = PyQtBrowser(parent)
    win.load_url(url_path)
    win.exec()
    return win
