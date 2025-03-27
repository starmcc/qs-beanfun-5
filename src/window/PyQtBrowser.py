from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtNetwork import QNetworkCookie, QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from src.client import RequestClient
from src.config.GlobalConfig import GLOBAL_CONFIG
from src.utils import BaseTools


class _CustomWebEngineView(QWebEngineView):
    def createWindow(self, web_window_type):
        return self


class _PyQtBrowser(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        BaseTools.set_basic_window(self)
        self.setMinimumSize(880, 550)
        self.setWindowTitle("浏览器")
        self.webView = _CustomWebEngineView()
        self.urlBar = QLineEdit()
        self.goButton = QPushButton("Go")
        self.backButton = QPushButton("←")
        self.forwardButton = QPushButton("→")
        layout = QVBoxLayout()
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.backButton)
        topLayout.addWidget(self.forwardButton)
        topLayout.addWidget(self.urlBar)
        topLayout.addWidget(self.goButton)
        layout.addLayout(topLayout)
        layout.addWidget(self.webView)
        self.setLayout(layout)
        self.backButton.clicked.connect(self.webView.back)
        self.forwardButton.clicked.connect(self.webView.forward)
        self.goButton.clicked.connect(self.__load_url)
        self.urlBar.returnPressed.connect(self.__load_url)
        self.webView.loadFinished.connect(self.__load_finish)
        self.webView.titleChanged.connect(self.__on_title_changed)
        self.__cookies_handler()
        self.show()

    def __on_title_changed(self, newTitle):
        self.setWindowTitle(newTitle)

    def __load_finish(self, status):
        self.urlBar.setText(self.webView.url().url())

    def __load_url(self):
        urlStr = self.urlBar.text()
        self.webView.load(self.build_url(urlStr))

    def load_url(self, urlStr: str):
        self.webView.load(self.build_url(urlStr))

    def load_html(self, html: str):
        self.webView.setHtml(html)

    def build_url(self, url) -> QUrl:
        if not url.startswith("http://") and not url.startswith("https://"):
            # 尝试连接 https，如果失败再尝试 http
            https_url = f"https://{url}"
            https_qurl = QUrl(https_url)
            request = QNetworkRequest(https_qurl)
            manager = QNetworkAccessManager()
            reply = manager.get(request)
            loop = QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec_()
            if reply.error() == QNetworkReply.NoError:
                return QUrl(https_qurl)
            else:
                return QUrl(f"http://{url}")
        else:
            return QUrl(url)

    def __cookies_handler(self):
        """
        获取 cookiestore
        """
        cookie_store = self.webView.page().profile().cookieStore()
        cookies = RequestClient.get_instance().client.cookies
        for cookie in cookies.jar:
            q_cookie = QNetworkCookie()
            q_cookie.setName(cookie.name.encode())
            q_cookie.setValue(cookie.value.encode())
            if cookie.domain is not None:
                q_cookie.setDomain(cookie.domain)
            q_cookie.setPath(cookie.path)
            if cookie.expires is not None:
                QDateTime.fromTime_t(int(cookie.expires))
            q_cookie.setSecure(cookie.secure)
            cookie_store.setCookie(q_cookie)


def open_browser(url_path: str, parent=None):
    GLOBAL_CONFIG.win_browser = _PyQtBrowser(parent)
    GLOBAL_CONFIG.win_browser.load_url(url_path)


def open_browser_html(html: str, parent=None):
    GLOBAL_CONFIG.win_browser = _PyQtBrowser(parent)
    GLOBAL_CONFIG.win_browser.load_html(html)