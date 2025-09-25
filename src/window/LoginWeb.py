import os
import tempfile
from http.cookiejar import Cookie

from PyQt5.QtCore import QUrl, QEventLoop, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QProgressBar, QPushButton)

from src.client import RequestClient
from src.config.GlobalConfig import GLOBAL_CONFIG, ActType
from src.utils import WinManager, BoxPop


class CustomWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.temp_dir = tempfile.TemporaryDirectory()  # 自动管理的临时目录
        self.profile = QWebEngineProfile(self.temp_dir.name, self)  # 绑定临时目录
        self.login_status = False
        # 禁用Cookie持久化
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        # 设置缓存和存储路径到临时目录
        self.profile.setCachePath(os.path.join(self.temp_dir.name, "cache"))
        self.profile.setPersistentStoragePath(os.path.join(self.temp_dir.name, "storage"))
        # 使用自定义Profile创建页面
        self.custom_page = QWebEnginePage(self.profile, self)
        self.setPage(self.custom_page)
        self.page().profile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}

    def createWindow(self, windowType):
        return self

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        key = cookie.name().data().decode('utf-8')
        value = cookie.value().data().decode('utf-8')
        self.cookies[(key, str(cookie.domain()))] = value  # 将cookie保存到字典里
        if key == "bfWebToken":
            GLOBAL_CONFIG.bf_web_token = value
            if GLOBAL_CONFIG.bf_web_token:
                self.login_status = True
                self.parent().finished_login.emit()

    def sync_httpx_cookies(self):
        jar = RequestClient.get_instance().client.cookies.jar
        jar.clear()
        for (key, domain), value in self.cookies.items():
            cookie = Cookie(
                name=key,  # cookie名称
                value=value,  # cookie值
                domain=domain,
                path="/",
                secure=False,
                expires=None,
                version=0,  # 版本号，默认0
                port=None,  # 端口，None表示不限制
                port_specified=False,  # 是否指定端口
                domain_specified=True,  # 是否指定域名
                domain_initial_dot=False,  # 域名是否以点开头
                path_specified=True,  # 是否指定路径
                discard=False,  # 是否会话结束后丢弃
                comment=None,  # 注释
                comment_url=None,  # 注释URL
                rest={},  # 其他属性
                rfc2109=False  # 是否遵循RFC2109标准
            )
            jar.set_cookie(cookie)

    def clear_all_data(self):
        self.cookies.clear()  # 清除内存Cookie
        self.profile.cookieStore().deleteAllCookies()  # 清除Profile中的Cookie
        self.profile.clearAllVisitedLinks()  # 清除访问记录
        if hasattr(self, 'temp_dir'):
            try:
                self.temp_dir.cleanup()  # 清理临时目录
            except Exception as e:
                print(f"清理临时文件失败: {e}")


class LoginWeb(QDialog):
    finished_login = pyqtSignal()
    _instance = None

    def __init__(self, parent):
        if LoginWeb._instance is not None:
            raise Exception("LoginWeb窗口只能打开一个！")
        super().__init__(parent)
        LoginWeb._instance = self
        GLOBAL_CONFIG.bf_web_token = None
        # 设置基本窗口属性
        self.setup_window()
        # 初始化界面组件
        self.init_ui()
        # 连接信号和槽
        self.connect_signals()

    def setup_window(self):
        WinManager.set_basic_window(self)
        self.setMinimumSize(1024, 800)
        type_act = '香港'
        if GLOBAL_CONFIG.now_login_type == ActType.TW.value:
            type_act = "台湾"
        self.setWindowTitle(WinManager.translate(f"{type_act}游戏橘子 - 登入"))

    def init_ui(self):
        # 创建界面组件
        self.web_view = CustomWebEngineView(self)
        self.progress_bar = QProgressBar()
        self.enter_btn = QPushButton(WinManager.translate("确认登入状态(如未自动跳转请成功登入后点击此处)"))
        self.enter_btn.setFixedHeight(38)

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

        # 布局设置
        main_layout = QVBoxLayout()
        botton_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        botton_layout.setContentsMargins(0, 0, 0, 0)
        botton_layout.setSpacing(0)
        botton_layout.addWidget(self.enter_btn)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.web_view)
        main_layout.addLayout(botton_layout)
        self.setLayout(main_layout)

    def connect_signals(self):
        self.web_view.loadFinished.connect(self.on_load_finished)
        self.web_view.loadProgress.connect(self.on_load_progress)
        self.web_view.loadStarted.connect(self.on_load_started)
        self.enter_btn.clicked.connect(self.on_login_enter)
        self.finished_login.connect(self.on_login_enter)

    def on_login_enter(self, event=None):
        if GLOBAL_CONFIG.bf_web_token:
            self.web_view.sync_httpx_cookies()
            self.parent().login_go_to_main_event.emit()
            self.close()
        else:
            BoxPop.info(self, "請先在網頁進行登入\n登入成功後在點此處完成登入")

    def on_load_started(self):
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def on_load_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress >= 100:
            self.progress_bar.hide()

    def normalize_url(self, url_str):
        url = QUrl(url_str)
        host = url.host()
        if not host:
            return url_str.rstrip('/')
        port = url.port()
        scheme = url.scheme().lower()
        default_port = 80 if scheme == 'http' else 443 if scheme == 'https' else -1
        if port != -1 and port != default_port:
            host += f":{port}"
        path = url.path().rstrip('/')
        normalized = f"{host}{path}" if path else host
        return normalized

    def on_load_finished(self, status):
        self.progress_bar.hide()

    def load_url(self, url_str: str):
        self.web_view.load(self.build_url(url_str))

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

    def closeEvent(self, event: QCloseEvent):
        if hasattr(self, 'web_view'):
            self.web_view.clear_all_data()
            self.web_view.stop()
            self.web_view.deleteLater()
        LoginWeb._instance = None
        event.accept()


def open_login_page(url_path: str, parent):
    if LoginWeb._instance is not None:
        LoginWeb._instance.showNormal()
        LoginWeb._instance.raise_()
        return LoginWeb._instance
    login_Web = LoginWeb(parent)
    login_Web.load_url(url_path)
    login_Web.show()
    return login_Web
