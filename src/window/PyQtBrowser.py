import logging

from PyQt5.QtCore import QUrl, QEventLoop, QDateTime
from PyQt5.QtNetwork import QNetworkCookie, QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

from src.client import RequestClient
from src.config.GlobalConfig import GLOBAL_CONFIG
from src.utils import BaseTools


class CustomWebEngineView(QWebEngineView):
    def createWindow(self, web_window_type):
        new_view = CustomWebEngineView()
        return new_view


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
        BaseTools.set_basic_window(self)
        self.setMinimumSize(880, 550)
        self.setWindowTitle("浏览器")

    def init_ui(self):
        # 创建界面组件
        self.web_view = CustomWebEngineView()
        self.url_bar = QLineEdit()
        self.go_button = QPushButton("Enter")
        self.back_button = QPushButton("后退")
        self.forward_button = QPushButton("前进")
        self.refresh_button = QPushButton("刷新")

        # 设置样式表
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 6px 12px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                cursor: pointer;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 6px;
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QDialog {
                background-color: #f4f4f4;
            }
        """)

        # 布局设置
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(8)

        top_layout.addWidget(self.back_button)
        top_layout.addWidget(self.forward_button)
        top_layout.addWidget(self.refresh_button)
        top_layout.addWidget(self.url_bar)
        top_layout.addWidget(self.go_button)
        main_layout.addLayout(top_layout)
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

    def on_title_changed(self, new_title):
        self.setWindowTitle(new_title)

    def on_load_finished(self, status):
        self.url_bar.setText(self.web_view.url().url())

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
            logging.error(f"处理 cookies 时出现错误: {e}")


def open_browser(url_path: str, parent=None):
    GLOBAL_CONFIG.win_browser = PyQtBrowser(parent)
    GLOBAL_CONFIG.win_browser.load_url(url_path)
    GLOBAL_CONFIG.win_browser.show()


def open_browser_html(html: str, parent=None):
    GLOBAL_CONFIG.win_browser = PyQtBrowser(parent)
    GLOBAL_CONFIG.win_browser.load_html(html)
    GLOBAL_CONFIG.win_browser.show()
