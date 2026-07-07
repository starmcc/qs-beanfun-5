import logging
import os

from PySide6.QtCore import QUrl, QEventLoop, QDateTime
from PySide6.QtGui import QCloseEvent
from PySide6.QtNetwork import QNetworkCookie, QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QProgressBar)

from src.client import RequestClient
from src.utils import WinManager


class CustomWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.profile_dir = os.path.expanduser(r"~\.qt_beanfun_profile")
        self.profile = QWebEngineProfile(self.profile_dir, self)
        chrome_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        self.profile.setHttpUserAgent(chrome_ua)
        self.profile.setHttpAcceptLanguage("zh-TW,zh;q=0.9,en;q=0.8")

    def createWindow(self, windowType):
        return self


class PyQtBrowser(QDialog):
    _instance = None

    def __init__(self, parent=None):
        if PyQtBrowser._instance is not None:
            raise Exception("PyQtBrowser窗口只能打开一个")
        super().__init__(parent)
        PyQtBrowser._instance = self
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
        main_layout.setContentsMargins(3, 3, 3, 3)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(3)

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
        """构建URL，使用共享的网络管理器并确保资源正确清理"""
        if not url or not isinstance(url, str):
            return QUrl()

        # 如果已经是完整URL，直接返回
        if url.startswith(("http://", "https://")):
            return QUrl(url)

        # 创建一次性的网络管理器
        manager = QNetworkAccessManager(self)
        reply = None
        loop = None

        try:
            # 先尝试HTTPS
            https_url = f"https://{url}"
            https_qurl = QUrl(https_url)
            request = QNetworkRequest(https_qurl)
            reply = manager.get(request)

            # 使用事件循环等待请求完成
            loop = QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec()

            # 修复Qt6枚举：QNetworkReply.NoError → QNetworkReply.NetworkError.NoError
            if reply.error() == QNetworkReply.NetworkError.NoError:
                return https_qurl
            else:
                # HTTPS失败，回退到HTTP
                return QUrl(f"http://{url}")

        except Exception as e:
            logging.error(f"URL构建失败: {str(e)}")
            # 发生异常时回退到HTTP
            return QUrl(f"http://{url}")
        finally:
            # 确保资源正确清理
            if reply:
                reply.deleteLater()
            if loop:
                loop.deleteLater()

    def handle_cookies(self):
        """
        获取 cookiestore 并将 requests 的 Cookie 同步到 Qt 的 QNetworkCookieStore
        """
        try:
            # 获取 Qt 的 CookieStore
            cookie_store = self.web_view.page().profile().cookieStore()
            # 获取 requests 客户端的 Cookies
            cookies = RequestClient.get_instance().client.cookies

            # 遍历 requests 的 RequestsCookieJar
            for cookie in cookies:
                # 初始化 Qt 的 QNetworkCookie
                q_cookie = QNetworkCookie()

                # 1. 设置 Cookie 名称和值
                q_cookie.setName(cookie.name.encode('utf-8'))
                q_cookie.setValue(cookie.value.encode('utf-8'))

                # 2. 设置域名
                if cookie.domain:
                    q_cookie.setDomain(cookie.domain)

                # 3. 设置路径
                q_cookie.setPath(cookie.path if cookie.path else '/')

                # 4. Qt6 废弃 fromTime_t，替换为 fromSecsSinceEpoch
                if cookie.expires:
                    expiration = QDateTime.fromSecsSinceEpoch(int(cookie.expires))
                    q_cookie.setExpirationDate(expiration)

                # 5. 设置是否为 HTTPS 安全 Cookie
                q_cookie.setSecure(cookie.secure)

                # 6. 将 Qt Cookie 写入 CookieStore
                cookie_store.setCookie(q_cookie)

        except Exception as e:
            logging.error(f"处理 cookies 时出现错误: {str(e)}")

    def closeEvent(self, event: QCloseEvent):
        self.web_view.deleteLater()
        PyQtBrowser._instance = None
        event.accept()


def open_browser(url_path: str, parent=None):
    # 1. 检查是否已有存活的PyQtBrowser实例
    if PyQtBrowser._instance is not None:
        PyQtBrowser._instance.showNormal()
        PyQtBrowser._instance.raise_()
        PyQtBrowser._instance.load_url(url_path)
        return PyQtBrowser._instance
    win_browser = PyQtBrowser(parent)
    win_browser.load_url(url_path)
    win_browser.exec()