import logging

from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

# ── 浏览器指纹反检测 JS ──
STEALTH_JS = r"""
(function() {
    'use strict';
    const handler = {
        has: (obj, prop) => prop === 'webdriver' ? false : prop in obj,
        get: (obj, prop) => prop === 'webdriver' ? undefined : obj[prop],
        ownKeys: (obj) => Reflect.ownKeys(obj).filter(k => k !== 'webdriver'),
        getOwnPropertyDescriptor: (obj, prop) =>
            prop === 'webdriver' ? undefined : Object.getOwnPropertyDescriptor(obj, prop)
    };
    navigator.__proto__ = new Proxy(navigator.__proto__, handler);
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
    window.chrome = {
        runtime: { onConnect: { addListener: () => {} }, onMessage: { addListener: () => {} } },
        webstore: {},
        app: { isInstalled: false, InstallState: { DISABLED: 'disabled', INSTALLED: 'installed', NOT_INSTALLED: 'not_installed' }, RunningState: { CANNOT_RUN: 'cannot_run', READY_TO_RUN: 'ready_to_run', RUNNING: 'running' } },
        csi: () => ({}),
        loadTimes: () => ({ requestTime: Date.now() / 1000, startLoadTime: Date.now() / 1000, commitLoadTime: Date.now() / 1000, finishDocumentLoadTime: Date.now() / 1000, finishLoadTime: Date.now() / 1000, firstPaintTime: Date.now() / 1000, firstPaintAfterLoadTime: 0, navigationType: 'Other', wasFetchedViaSpdy: false, wasNpnNegotiated: false, npnNegotiatedProtocol: 'unknown', connectionInfo: 'http/1.1', wasAlternateProtocolAvailable: false })
    };
    Object.defineProperty(navigator, 'plugins', {
        get: () => {
            const PluginArray = function() {};
            PluginArray.prototype = Array.prototype;
            const arr = new PluginArray();
            arr.item = i => arr[i];
            arr.namedItem = n => arr.find(p => p.name === n);
            arr.refresh = () => {};
            arr.push(
                { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format', length: 1, 0: { type: 'application/pdf', suffixes: 'pdf', description: 'Portable Document Format' } },
                { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: '', length: 1, 0: { type: 'application/pdf', suffixes: 'pdf', description: '' } },
                { name: 'Native Client', filename: 'internal-nacl-plugin', description: '', length: 2, 0: { type: 'application/x-nacl', suffixes: '', description: 'Native Client Executable' }, 1: { type: 'application/x-pnacl', suffixes: '', description: 'Portable Native Client Executable' } }
            );
            return arr;
        }
    });
    Object.defineProperty(navigator, 'mimeTypes', {
        get: () => {
            const MimeTypeArray = function() {};
            MimeTypeArray.prototype = Array.prototype;
            const arr = new MimeTypeArray();
            arr.item = i => arr[i];
            arr.namedItem = n => arr.find(m => m.type === n);
            arr.push(
                { type: 'application/pdf', suffixes: 'pdf', description: 'Portable Document Format' },
                { type: 'text/pdf', suffixes: 'pdf', description: 'Portable Document Format' }
            );
            return arr;
        }
    });
    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
    Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 0 });
    Object.defineProperty(navigator, 'language', { get: () => 'zh-TW' });
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-TW', 'zh', 'en'] });
    Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
    const origQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = function(params) {
        return origQuery.call(this, params).then(result => {
            const overrides = { notifications: 'prompt', midi: 'prompt', camera: 'prompt', microphone: 'prompt' };
            if (overrides[params.name]) Object.defineProperty(result, 'state', { get: () => overrides[params.name] });
            return result;
        });
    };
    const getParameterProxies = {
        [WebGLRenderingContext.prototype.VENDOR]: 'Google Inc. (Intel)',
        [WebGLRenderingContext.prototype.RENDERER]: 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
    };
    const origGetParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(p) {
        return getParameterProxies[p] || origGetParameter.call(this, p);
    };
    if (typeof WebGL2RenderingContext !== 'undefined') {
        const gp2 = { [WebGL2RenderingContext.prototype.VENDOR]: 'Google Inc. (Intel)', [WebGL2RenderingContext.prototype.RENDERER]: 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)' };
        const origGP2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(p) { return gp2[p] || origGP2.call(this, p); };
    }
    const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function() {
        const ctx = this.getContext('2d');
        if (ctx && this.width > 0 && this.height > 0) {
            const imageData = ctx.getImageData(0, 0, this.width, this.height);
            for (let i = 0; i < imageData.data.length; i += 4) imageData.data[i] ^= (i % 3 === 0 ? 1 : 0);
            ctx.putImageData(imageData, 0, 0);
        }
        return origToDataURL.apply(this, arguments);
    };
    function setRecaptchaLang() {
        const iframe = document.querySelector('iframe[src*="recaptcha"]');
        if (!iframe) return;
        try { const url = new URL(iframe.src); if (url.searchParams.get('hl') !== 'zh-TW') { url.searchParams.set('hl', 'zh-TW'); iframe.src = url.toString(); } } catch(e) {}
    }
    setTimeout(setRecaptchaLang, 800);
    setTimeout(setRecaptchaLang, 2000);
    new MutationObserver(setRecaptchaLang).observe(document.body || document.documentElement, { childList: true, subtree: true });
})();
"""


class BaseWebEngineView(QWebEngineView):
    """共享的浏览器引擎基类：无持久化存储、反检测 JS、Cookie 同步。

    每次创建实例都是全新的浏览器会话（off-the-record profile），
    不会保留任何本地缓存、Cookie 或存储。"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 使用 off-the-record profile：每次都是全新会话，无磁盘缓存
        self.profile = QWebEngineProfile(self)
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        )
        self.profile.setHttpAcceptLanguage("zh-TW,zh;q=0.9,en;q=0.8")

        self.custom_page = QWebEnginePage(self.profile, self)
        self.setPage(self.custom_page)

        settings = self.page().settings()
        attr = QWebEngineSettings.WebAttribute
        settings.setAttribute(attr.JavascriptEnabled, True)
        settings.setAttribute(attr.LocalStorageEnabled, True)
        settings.setAttribute(attr.AllowRunningInsecureContent, True)
        settings.setAttribute(attr.JavascriptCanAccessClipboard, True)
        settings.setAttribute(attr.AllowGeolocationOnInsecureOrigins, True)
        settings.setAttribute(attr.PlaybackRequiresUserGesture, False)
        settings.setAttribute(attr.WebGLEnabled, True)

        self.cookies = {}
        self._stealth_injected = False

        self.profile.cookieStore().cookieAdded.connect(self._on_cookie_added)
        self.page().loadFinished.connect(self._on_load_finished)

    # ── Cookie ──

    def _on_cookie_added(self, cookie):
        from src.config.GlobalConfig import GLOBAL_CONFIG
        key = cookie.name().data().decode("utf-8")
        value = cookie.value().data().decode("utf-8")
        domain = str(cookie.domain())
        self.cookies[(key, domain)] = value
        if key == "bfWebToken":
            GLOBAL_CONFIG.bf_web_token = value

    def sync_cookies_to_requests(self):
        """将浏览器 Cookie 同步到 requests 客户端"""
        from src.client import RequestClient
        try:
            jar = RequestClient.get_instance().client.cookies
            jar.clear()
            for (key, domain), value in self.cookies.items():
                secure = domain.endswith("beanfun.com") or domain.endswith("google.com")
                jar.set(name=key, value=value, domain=domain, path="/", secure=secure,
                        expires=None, rest={}, version=0)
            logging.info("Cookie 已同步到 requests 客户端")
        except Exception as e:
            logging.error(f"同步 Cookie 失败: {e}")

    def sync_cookies_from_requests(self):
        """将 requests 客户端的 Cookie 同步到浏览器"""
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
        except Exception as e:
            logging.error(f"同步 Cookie 到浏览器失败: {e}")

    # ── 反检测 JS ──

    def _on_load_finished(self, ok):
        if not ok or self._stealth_injected:
            return
        self._stealth_injected = True
        self.page().runJavaScript(STEALTH_JS)

    # ── 弹窗拦截 ──

    def createWindow(self, windowType):
        return self
