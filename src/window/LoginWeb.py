import logging
import os

from PySide6.QtCore import QUrl
from PySide6.QtGui import QCloseEvent
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QProgressBar, QPushButton

# ── Chromium 启动参数：反自动化检测 + 模拟真实浏览器环境 ──
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--disable-blink-features=AutomationControlled "
    "--no-first-run --no-default-browser-check "
    "--disable-automation "
    "--exclude-switches=enable-automation "
    "--disable-dev-shm-usage "
    "--disable-features=TranslateUI "
    "--enable-webgl "
    "--ignore-gpu-blocklist "
    "--enable-gpu-rasterization "
    "--enable-features=NetworkService,NetworkServiceInProcess "
    "--use-gl=swiftshader "
    "--window-size=1024,800"
)
os.environ["QT_LOGGING_RULES"] = "qt.webengine.debug=false;qt.webengine.warning=false;qt.webengine.error=false"

from src.client import RequestClient
from src.config.GlobalConfig import GLOBAL_CONFIG, ActType
from src.utils import WinManager, BoxPop


# ── 浏览器指纹反检测 JS（注入到每个页面） ──
STEALTH_JS = r"""
(function() {
    'use strict';

    // 1. 彻底移除 navigator.webdriver（正常浏览器不存在此属性）
    const handler = {
        has: (obj, prop) => prop === 'webdriver' ? false : prop in obj,
        get: (obj, prop) => prop === 'webdriver' ? undefined : obj[prop],
        ownKeys: (obj) => Reflect.ownKeys(obj).filter(k => k !== 'webdriver'),
        getOwnPropertyDescriptor: (obj, prop) =>
            prop === 'webdriver' ? undefined : Object.getOwnPropertyDescriptor(obj, prop)
    };
    navigator.__proto__ = new Proxy(navigator.__proto__, handler);

    // 2. 移除 Chrome DevTools Protocol 残留
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;

    // 3. 模拟真实 Chrome window.chrome 对象
    window.chrome = {
        runtime: { onConnect: { addListener: () => {} }, onMessage: { addListener: () => {} } },
        webstore: {},
        app: { isInstalled: false, InstallState: { DISABLED: 'disabled', INSTALLED: 'installed', NOT_INSTALLED: 'not_installed' }, RunningState: { CANNOT_RUN: 'cannot_run', READY_TO_RUN: 'ready_to_run', RUNNING: 'running' } },
        csi: () => ({}),
        loadTimes: () => ({ requestTime: Date.now() / 1000, startLoadTime: Date.now() / 1000, commitLoadTime: Date.now() / 1000, finishDocumentLoadTime: Date.now() / 1000, finishLoadTime: Date.now() / 1000, firstPaintTime: Date.now() / 1000, firstPaintAfterLoadTime: 0, navigationType: 'Other', wasFetchedViaSpdy: false, wasNpnNegotiated: false, npnNegotiatedProtocol: 'unknown', connectionInfo: 'http/1.1', wasAlternateProtocolAvailable: false })
    };

    // 4. 模拟真实插件列表（Chrome 标准插件）
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

    // 5. 模拟 mimeTypes
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

    // 6. 模拟硬件指纹
    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
    Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 0 });

    // 7. 模拟语言（繁体中文优先）
    Object.defineProperty(navigator, 'language', { get: () => 'zh-TW' });
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-TW', 'zh', 'en'] });

    // 8. 模拟 platform
    Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });

    // 9. 权限查询修复
    const origQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = function(params) {
        return origQuery.call(this, params).then(result => {
            const overrides = { notifications: 'prompt', midi: 'prompt', camera: 'prompt', microphone: 'prompt' };
            if (overrides[params.name]) {
                Object.defineProperty(result, 'state', { get: () => overrides[params.name] });
            }
            return result;
        });
    };

    // 10. 覆盖 WebGL 指纹为常见 GPU（Intel UHD / NVIDIA）
    const getParameterProxies = {
        [WebGLRenderingContext.prototype.VENDOR]: 'Google Inc. (Intel)',
        [WebGLRenderingContext.prototype.RENDERER]: 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
        [WebGL2RenderingContext.prototype.VENDOR]: 'Google Inc. (Intel)',
        [WebGL2RenderingContext.prototype.RENDERER]: 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)'
    };
    const origGetParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(p) {
        return getParameterProxies[p] || origGetParameter.call(this, p);
    };
    if (typeof WebGL2RenderingContext !== 'undefined') {
        const origGetParameter2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(p) {
            return getParameterProxies[p] || origGetParameter2.call(this, p);
        };
    }

    // 11. Canvas 指纹轻微随机化（每次 toDataURL 加微小噪点，不影响视觉）
    const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function() {
        const ctx = this.getContext('2d');
        if (ctx && this.width > 0 && this.height > 0) {
            const imageData = ctx.getImageData(0, 0, this.width, this.height);
            for (let i = 0; i < imageData.data.length; i += 4) {
                imageData.data[i] ^= (i % 3 === 0 ? 1 : 0);
            }
            ctx.putImageData(imageData, 0, 0);
        }
        return origToDataURL.apply(this, arguments);
    };

    // 12. 强制 reCAPTCHA 使用繁体中文
    function setRecaptchaLang() {
        const iframe = document.querySelector('iframe[src*="recaptcha"]');
        if (!iframe) return;
        try {
            const url = new URL(iframe.src);
            if (url.searchParams.get('hl') !== 'zh-TW') {
                url.searchParams.set('hl', 'zh-TW');
                iframe.src = url.toString();
            }
        } catch(e) {}
    }
    setTimeout(setRecaptchaLang, 800);
    setTimeout(setRecaptchaLang, 2000);
    new MutationObserver(setRecaptchaLang).observe(document.body || document.documentElement, { childList: true, subtree: true });
})();
"""


class CustomWebEngineView(QWebEngineView):
    """内置浏览器视图，配置持久化 Profile、反检测 JS 注入、Cookie 同步"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.profile_dir = os.path.expanduser(r"~\.qt_beanfun_profile")
        self.profile = QWebEngineProfile(self.profile_dir, self)
        self.cookies = {}
        self._stealth_injected = False

        # ── HTTP 头伪装 ──
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        )
        self.profile.setHttpAcceptLanguage("zh-TW,zh;q=0.9,en;q=0.8")

        # ── 持久化存储 ──
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        self.profile.setCachePath(os.path.join(self.profile_dir, "cache"))
        self.profile.setPersistentStoragePath(os.path.join(self.profile_dir, "storage"))

        # ── 页面设置 ──
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

        # ── 信号 ──
        self.profile.cookieStore().cookieAdded.connect(self._on_cookie_added)
        self.page().loadFinished.connect(self._on_load_finished)

    # ── Cookie 处理 ──

    def _on_cookie_added(self, cookie):
        key = cookie.name().data().decode("utf-8")
        value = cookie.value().data().decode("utf-8")
        domain = str(cookie.domain())
        self.cookies[(key, domain)] = value
        if key == "bfWebToken":
            GLOBAL_CONFIG.bf_web_token = value

    def sync_requests_cookies(self):
        """将浏览器 Cookie 同步到 requests 客户端"""
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

    def clear_memory_cookies(self):
        self.cookies.clear()
        self.profile.cookieStore().deleteAllCookies()
        self._stealth_injected = False

    # ── 反检测 JS 注入 ──

    def _on_load_finished(self, ok):
        if not ok or self._stealth_injected:
            return
        self._stealth_injected = True
        self.page().runJavaScript(STEALTH_JS)

    # ── 弹窗拦截（在本窗口打开） ──

    def createWindow(self, windowType):
        return self


class LoginWeb(QDialog):
    """内置浏览器登录窗口（单例）"""

    _instance = None

    def __init__(self, parent):
        if LoginWeb._instance is not None:
            raise Exception("LoginWeb 窗口只能打开一个")
        super().__init__(parent)
        LoginWeb._instance = self
        GLOBAL_CONFIG.bf_web_token = None
        self._setup_window()
        self._init_ui()
        self._connect_signals()

    # ── 窗口设置 ──

    def _setup_window(self):
        WinManager.set_basic_window(self)
        self.setMinimumSize(1024, 800)
        type_act = "香港" if GLOBAL_CONFIG.now_login_type != ActType.TW.value else "台湾"
        self.setWindowTitle(WinManager.translate(f"{type_act}游戏橘子 - 登入"))

    # ── UI 构建 ──

    def _init_ui(self):
        self.web_view = CustomWebEngineView(self)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet("""
            QProgressBar { background-color: #E5E6EB; border: none; border-radius: 1px; }
            QProgressBar::chunk { background-color: #165DFF; border-radius: 1px; }
        """)
        self.progress_bar.hide()

        self.enter_btn = QPushButton(WinManager.translate("确认登入状态(请成功登入后点击此处)"))
        self.enter_btn.setFixedHeight(38)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.web_view, 1)
        layout.addWidget(self.enter_btn)

    # ── 信号连接 ──

    def _connect_signals(self):
        self.web_view.loadStarted.connect(self._on_load_started)
        self.web_view.loadProgress.connect(self._on_load_progress)
        self.web_view.loadFinished.connect(self._on_load_finished)
        self.enter_btn.clicked.connect(self._on_login_enter)

    # ── 加载进度 ──

    def _on_load_started(self):
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def _on_load_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress >= 100:
            self.progress_bar.hide()

    def _on_load_finished(self, status):
        self.progress_bar.hide()

    # ── 登录确认 ──

    def _on_login_enter(self):
        if GLOBAL_CONFIG.bf_web_token:
            self.web_view.sync_requests_cookies()
            self.parent().login_go_to_main_event.emit()
            self.close()
        else:
            BoxPop.info(self, "請先在網頁進行登入\n登入成功後再點此處完成登入")

    # ── URL 加载 ──

    def load_url(self, url: str):
        if url.startswith(("http://", "https://")):
            self.web_view.load(QUrl(url))
        else:
            self.web_view.load(QUrl(f"https://{url}"))

    # ── 关闭清理 ──

    def closeEvent(self, event: QCloseEvent):
        if hasattr(self, "web_view"):
            self.web_view.stop()
            self.web_view.load(QUrl("about:blank"))
            self.web_view.clear_memory_cookies()
            self.web_view.deleteLater()
        LoginWeb._instance = None
        event.accept()


def open_login_page(url_path: str, parent):
    """打开登录页面（单例复用）"""
    if LoginWeb._instance is not None:
        LoginWeb._instance.showNormal()
        LoginWeb._instance.raise_()
        return LoginWeb._instance
    win = LoginWeb(parent)
    win.load_url(url_path)
    win.show()
    return win
