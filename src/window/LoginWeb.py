import logging
import os
from PyQt6.QtCore import QUrl, QEventLoop, Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QProgressBar, QPushButton, QLabel)

# 放在最顶部，所有Qt导入之前，解决GPU/GLES报错、虚拟机渲染失败
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--disable-blink-features=AutomationControlled "
    "--no-first-run --no-default-browser-check "
    "--disable-automation --disable-ui-devtools "
    "--exclude-switches=enable-automation "
    "--disable-dev-shm-usage "
    "--window-size=1024,800 "
    "--ignore-gpu-blacklist "
    "--enable-webgl "
    "--disable-gpu-sandbox "
    "--disable-gpu --disable-software-rasterizer"
)
# 屏蔽WebEngine冗余错误日志
os.environ["QT_LOGGING_RULES"] = "qt.webengine.debug=false;qt.webengine.warning=false;qt.webengine.error=false"

from src.client import RequestClient
from src.config.GlobalConfig import GLOBAL_CONFIG, ActType
from src.utils import WinManager, BoxPop


class CustomWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 持久化配置目录
        self.profile_dir = os.path.expanduser(r"~\.qt_beanfun_profile")
        self.profile = QWebEngineProfile(self.profile_dir, self)

        # 繁体中文UA+语言头
        chrome_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        self.profile.setHttpUserAgent(chrome_ua)
        self.profile.setHttpAcceptLanguage("zh-TW,zh;q=0.9,en;q=0.8")

        # 网页基础权限 Qt6 修复
        settings = self.page().settings()
        attr = QWebEngineSettings.WebAttribute
        settings.setAttribute(attr.JavascriptEnabled, True)
        settings.setAttribute(attr.LocalStorageEnabled, True)
        settings.setAttribute(attr.AllowRunningInsecureContent, True)
        settings.setAttribute(attr.JavascriptCanAccessClipboard, True)
        settings.setAttribute(attr.AllowGeolocationOnInsecureOrigins, True)

        # 开启持久Cookie Qt6枚举不变
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        self.profile.setCachePath(os.path.join(self.profile_dir, "cache"))
        self.profile.setPersistentStoragePath(os.path.join(self.profile_dir, "storage"))

        self.custom_page = QWebEnginePage(self.profile, self)
        self.setPage(self.custom_page)
        self.page().profile().cookieStore().cookieAdded.connect(self.onCookieAdd)

        self.cookies = {}
        self.load_finished_flag = False
        self.page().loadFinished.connect(self.inject_full_stealth_js)

    def inject_full_stealth_js(self, ok):
        if not ok or self.load_finished_flag:
            return
        self.load_finished_flag = True

        # 反检测JS
        script = """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        delete navigator.__webdriver;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;

        // 模拟原生Chrome window.chrome对象
        window.chrome = {
            runtime: {},
            webstore: {},
            app: {},
            csi: () => {},
            loadTimes: () => {}
        };

        // 模拟真实PDF插件列表
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {name: "Chrome PDF Plugin", description: "Portable Document Format", filename: "internal-pdf-viewer"},
                {name: "Chrome PDF Viewer", description: "", filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai"}
            ]
        });

        // 权限检测返回值
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (params) => originalQuery(params).then(res => {
            if (params.name === 'notifications') res.state = 'prompt';
            return res;
        });

        // 强制繁体中文
        function setTwCaptchaLang(){
            const iframe = document.querySelector('iframe[src*="recaptcha"]');
            if(!iframe) return;
            const url = new URL(iframe.src);
            url.searchParams.set('hl','zh-TW');
            iframe.src = url.toString();
        }
        setTimeout(setTwCaptchaLang, 1000);
        """
        self.page().runJavaScript(script)

    def createWindow(self, windowType):
        return self

    def onCookieAdd(self, cookie):
        key = cookie.name().data().decode('utf-8')
        value = cookie.value().data().decode('utf-8')
        domain = str(cookie.domain())
        self.cookies[(key, domain)] = value
        if key == "bfWebToken":
            GLOBAL_CONFIG.bf_web_token = value

    def sync_requests_cookies(self):
        try:
            cookies_jar = RequestClient.get_instance().client.cookies
            cookies_jar.clear()
            for (key, domain), value in self.cookies.items():
                secure = domain.endswith("beanfun.com") or domain.endswith("google.com")
                cookies_jar.set(
                    name=key, value=value, domain=domain, path="/", secure=secure,
                    expires=None, rest={}, version=0
                )
            logging.info("Cookie 已成功同步到 requests 客户端")
        except Exception as e:
            logging.error(f"同步 Cookie 到 requests 时出错: {str(e)}")

    def clear_memory_cookies(self):
        # 仅清空内存Cookie，保留磁盘持久缓存
        self.cookies.clear()
        self.profile.cookieStore().deleteAllCookies()
        self.load_finished_flag = False


class LoginWeb(QDialog):
    _instance = None

    def __init__(self, parent):
        if LoginWeb._instance is not None:
            raise Exception("LoginWeb窗口只能打开一个")
        super().__init__(parent)
        LoginWeb._instance = self
        GLOBAL_CONFIG.bf_web_token = None
        self.setup_window()
        self.init_ui()
        self.connect_signals()

    def setup_window(self):
        WinManager.set_basic_window(self)
        self.setMinimumSize(1024, 800)
        type_act = '香港'
        if GLOBAL_CONFIG.now_login_type == ActType.TW.value:
            type_act = "台湾"
        self.setWindowTitle(WinManager.translate(f"{type_act}游戏橘子 - 登入"))

    def init_ui(self):
        self.web_view = CustomWebEngineView(self)
        self.progress_bar = QProgressBar()
        self.enter_btn = QPushButton(WinManager.translate("确认登入状态(请成功登入后点击此处)"))
        self.enter_btn.setFixedHeight(38)

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
        self.progress_bar.hide()

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

    def on_login_enter(self, event=None):
        if GLOBAL_CONFIG.bf_web_token:
            self.web_view.sync_requests_cookies()
            self.parent().login_go_to_main_event.emit()
            self.close()
        else:
            BoxPop.info(self, "請先在網頁進行登入\n登入成功後再點此處完成登入")

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
        if not url or not isinstance(url, str):
            return QUrl()
        if url.startswith(("http://", "https://")):
            return QUrl(url)

        manager = QNetworkAccessManager(self)
        reply = None
        loop = None
        try:
            https_url = f"https://{url}"
            https_qurl = QUrl(https_url)
            request = QNetworkRequest(https_qurl)
            reply = manager.get(request)
            loop = QEventLoop()
            reply.finished.connect(loop.quit)
            # Qt6 废弃 exec_()
            loop.exec()
            # Qt6 网络枚举修复
            if reply.error() == QNetworkReply.NetworkError.NoError:
                return https_qurl
            else:
                return QUrl(f"http://{url}")
        except Exception as e:
            logging.error(f"URL构建失败: {str(e)}")
            return QUrl(f"http://{url}")
        finally:
            if reply:
                reply.deleteLater()
            if loop:
                loop.deleteLater()

    def closeEvent(self, event: QCloseEvent):
        if hasattr(self, 'web_view'):
            self.web_view.stop()
            self.web_view.load(QUrl("about:blank"))
            # 仅清空内存Cookie，保留磁盘缓存目录
            self.web_view.clear_memory_cookies()
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