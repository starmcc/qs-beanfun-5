import logging

from PySide6.QtCore import QUrl, Signal
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView


class BaseWebEngineView(QWebEngineView):
    """极简浏览器引擎：defaultProfile、Cookie 同步、页面跳转感知。"""

    url_changed = Signal(str)
    title_changed = Signal(str)
    bf_token_ready = Signal()  # bfWebToken 捕获后发射

    def __init__(self, parent=None):
        super().__init__(parent)

        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        )
        self.profile.setHttpAcceptLanguage("zh-TW,zh;q=0.9,en;q=0.8")

        self.custom_page = QWebEnginePage(self.profile, self)
        self.setPage(self.custom_page)

        settings = self.page().settings()
        attr = QWebEngineSettings.WebAttribute
        settings.setAttribute(attr.JavascriptEnabled, True)
        settings.setAttribute(attr.LocalStorageEnabled, True)
        settings.setAttribute(attr.JavascriptCanOpenWindows, True)

        self.cookies = {}
        self.profile.cookieStore().cookieAdded.connect(self._on_cookie_added)
        self.urlChanged.connect(self._on_url_changed)
        self.titleChanged.connect(self._on_title_changed)

    def _on_cookie_added(self, cookie):
        from src.config.GlobalConfig import GLOBAL_CONFIG
        key = cookie.name().data().decode("utf-8")
        value = cookie.value().data().decode("utf-8")
        domain = str(cookie.domain())
        self.cookies[(key, domain)] = value
        if key == "bfWebToken":
            GLOBAL_CONFIG.bf_web_token = value
            logging.info(f"[BaseWebEngine] bfWebToken 已捕获: {value[:20]}...")
            self.bf_token_ready.emit()

    def _on_url_changed(self, url: QUrl):
        url_str = url.toString()
        if url_str and url_str != "about:blank":
            self.url_changed.emit(url_str)

    def _on_title_changed(self, title: str):
        if title:
            self.title_changed.emit(title)

    def sync_cookies_to_requests(self):
        from src.client import RequestClient
        try:
            jar = RequestClient.get_instance().client.cookies
            jar.clear()
            for (key, domain), value in self.cookies.items():
                jar.set(name=key, value=value, domain=domain, path="/")
            logging.info(f"[BaseWebEngine] Cookie 已同步 ({len(self.cookies)} 条)")
        except Exception as e:
            logging.error(f"[BaseWebEngine] 同步 Cookie 失败: {e}")

    def sync_cookies_from_requests(self):
        from src.client import RequestClient
        try:
            cookie_store = self.profile.cookieStore()
            from PySide6.QtCore import QDateTime
            from PySide6.QtNetwork import QNetworkCookie
            for cookie in RequestClient.get_instance().client.cookies:
                q_cookie = QNetworkCookie()
                q_cookie.setName(cookie.name.encode("utf-8"))
                q_cookie.setValue(cookie.value.encode("utf-8"))
                if cookie.domain:
                    q_cookie.setDomain(cookie.domain)
                q_cookie.setPath(cookie.path if cookie.path else "/")
                if cookie.expires:
                    q_cookie.setExpirationDate(QDateTime.fromSecsSinceEpoch(int(cookie.expires)))
                q_cookie.setSecure(cookie.secure)
                cookie_store.setCookie(q_cookie)
            logging.info("[BaseWebEngine] Cookie 已从 requests 同步到浏览器")
        except Exception as e:
            logging.error(f"[BaseWebEngine] 同步 Cookie 到浏览器失败: {e}")

    def createWindow(self, windowType):
        return self

    def navigate(self, url: str):
        if url.startswith(("http://", "https://")):
            self.load(QUrl(url))
        else:
            self.load(QUrl(f"https://{url}"))
