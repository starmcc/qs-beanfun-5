import logging

from PyQt5.QtCore import QUrl, QEventLoop, QDateTime
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtNetwork import QNetworkCookie, QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QProgressBar)

from src.client import RequestClient
from src.utils import WinManager


class CustomWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createWindow(self, windowType):
        return self


class PyQtBrowser(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置基本窗口属性
        self.setup_window()
        # 初始化界面组件
        self.init_ui()
        # 连接信号和槽
        self.connect_signals()
        # 处理 cookies
        self.handle_cookies()

    def setup_window(self):
        WinManager.set_basic_window(self)
        self.setMinimumSize(880, 550)
        self.setWindowTitle("浏览器")

    def init_ui(self):
        # 创建界面组件
        self.web_view = CustomWebEngineView(self)
        self.url_bar = QLineEdit()
        self.go_button = QPushButton("进入")
        self.back_button = QPushButton("←")
        self.forward_button = QPushButton("→")
        self.refresh_button = QPushButton("↻")
        self.progress_bar = QProgressBar()

        # 设置进度条样式
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #E5E6EB;
                border: none;
                border-radius: 1px;
            }
            QProgressBar::chunk {
                background-color: #165DFF;
                border-radius: 1px;
            }
        """)
        self.progress_bar.hide()  # 初始隐藏

        # 设置样式表 - 现代风格
        self.setStyleSheet("""
            QPushButton {
                background-color: #165DFF;
                color: white;
                border: none;
                padding: 6px 12px;
                font-size: 14px;
                border-radius: 4px;
                transition: background-color 0.2s;
            }
            QPushButton:hover {
                background-color: #4080FF;
            }
            QPushButton:pressed {
                background-color: #0E42D2;
            }
            QLineEdit {
                padding: 8px 10px;
                font-size: 14px;
                border: 1px solid #E5E6EB;
                border-radius: 4px;
                background-color: white;
                transition: border-color 0.2s;
            }
            QLineEdit:focus {
                border-color: #165DFF;
                outline: none;
            }
            QDialog {
                background-color: #F7F8FA;
            }
            QWidget {
                font-family: 'Microsoft YaHei', 'SimHei', sans-serif;
            }
        """)

        # 布局设置
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        top_layout.setContentsMargins(0, 0, 0, 4)
        top_layout.setSpacing(8)

        # 设置按钮最小宽度
        self.back_button.setMinimumWidth(36)
        self.forward_button.setMinimumWidth(36)
        self.refresh_button.setMinimumWidth(36)
        self.go_button.setMinimumWidth(60)

        top_layout.addWidget(self.back_button)
        top_layout.addWidget(self.forward_button)
        top_layout.addWidget(self.refresh_button)
        top_layout.addWidget(self.url_bar)
        top_layout.addWidget(self.go_button)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.web_view)
        self.setLayout(main_layout)

    def connect_signals(self):
        self.back_button.clicked.connect(self.web_view.back)
        self.forward_button.clicked.connect(self.web_view.forward)
        self.refresh_button.clicked.connect(self.web_view.reload)
        self.go_button.clicked.connect(self.load_url_from_bar)
        self.url_bar.returnPressed.connect(self.load_url_from_bar)
        self.web_view.loadFinished.connect(self.on_load_finished)
        self.web_view.titleChanged.connect(self.on_title_changed)
        self.web_view.loadProgress.connect(self.on_load_progress)
        self.web_view.loadStarted.connect(self.on_load_started)

    def on_title_changed(self, new_title):
        self.setWindowTitle(new_title)

    def on_load_started(self):
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def on_load_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress >= 100:
            self.progress_bar.hide()

    def on_load_finished(self, status):
        self.url_bar.setText(self.web_view.url().url())
        self.progress_bar.hide()

    def load_url_from_bar(self):
        url_str = self.url_bar.text()
        if url_str:
            self.web_view.load(self.build_url(url_str))

    def load_url(self, url_str: str):
        self.url_bar.setText(url_str)
        self.web_view.load(self.build_url(url_str))

    def load_html(self, html: str):
        self.web_view.setHtml(html)

    def build_url(self, url):
        if not url.startswith(("http://", "https://")):
            https_url = f"https://{url}"
            https_qurl = QUrl(https_url)
            request = QNetworkRequest(https_qurl)
            manager = QNetworkAccessManager(self)
            reply = manager.get(request)
            loop = QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec_()
            if reply.error() == QNetworkReply.NoError:
                reply.deleteLater()
                return https_qurl
            else:
                reply.deleteLater()
                return QUrl(f"http://{url}")
        return QUrl(url)

    def handle_cookies(self):
        """
        获取 cookiestore
        """
        try:
            cookie_store = self.web_view.page().profile().cookieStore()
            cookies = RequestClient.get_instance().client.cookies
            for cookie in cookies.jar:
                q_cookie = QNetworkCookie()
                q_cookie.setName(cookie.name.encode())
                q_cookie.setValue(cookie.value.encode())
                if cookie.domain:
                    q_cookie.setDomain(cookie.domain)
                q_cookie.setPath(cookie.path)
                if cookie.expires:
                    expiration = QDateTime.fromTime_t(int(cookie.expires))
                    q_cookie.setExpirationDate(expiration)
                q_cookie.setSecure(cookie.secure)
                cookie_store.setCookie(q_cookie)
        except Exception as e:
            logging.error(f"处理 cookies 时出现错误: {str(e)}")

    def closeEvent(self, event: QCloseEvent):
        self.web_view.deleteLater()
        event.accept()


def open_browser(url_path: str, parent=None):
    win_browser = PyQtBrowser(parent)
    win_browser.load_url(url_path)
    win_browser.show()
    return win_browser
