import logging

from PySide6.QtCore import QUrl, Signal
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

# ── 浏览器指纹反检测 JS（增强版） ──
STEALTH_JS = r"""
(function() {
    'use strict';

    // ── 1. 隐藏 webdriver 标记 ──
    const handler = {
        has: (obj, prop) => prop === 'webdriver' ? false : prop in obj,
        get: (obj, prop) => prop === 'webdriver' ? undefined : obj[prop],
        ownKeys: (obj) => Reflect.ownKeys(obj).filter(k => k !== 'webdriver'),
        getOwnPropertyDescriptor: (obj, prop) =>
            prop === 'webdriver' ? undefined : Object.getOwnPropertyDescriptor(obj, prop)
    };
    navigator.__proto__ = new Proxy(navigator.__proto__, handler);

    // ── 2. 删除 Chrome DevTools 检测变量 ──
    const cdcKeys = ['cdc_adoQpoasnfa76pfcZLmcfl_Array', 'cdc_adoQpoasnfa76pfcZLmcfl_Promise',
                     'cdc_adoQpoasnfa76pfcZLmcfl_Symbol', 'cdc_adoQpoasnfa76pfcZLmcfl_JSON',
                     'cdc_adoQpoasnfa76pfcZLmcfl_Object', 'cdc_adoQpoasnfa76pfcZLmcfl_Proxy'];
    cdcKeys.forEach(k => { try { delete window[k]; } catch(e) {} });

    // ── 3. 伪造 chrome.runtime ──
    window.chrome = {
        runtime: {
            onConnect: { addListener: () => {} },
            onMessage: { addListener: () => {} }
        },
        webstore: {},
        app: {
            isInstalled: false,
            InstallState: { DISABLED: 'disabled', INSTALLED: 'installed', NOT_INSTALLED: 'not_installed' },
            RunningState: { CANNOT_RUN: 'cannot_run', READY_TO_RUN: 'ready_to_run', RUNNING: 'running' }
        },
        csi: () => ({}),
        loadTimes: () => ({
            requestTime: Date.now() / 1000, startLoadTime: Date.now() / 1000,
            commitLoadTime: Date.now() / 1000, finishDocumentLoadTime: Date.now() / 1000,
            finishLoadTime: Date.now() / 1000, firstPaintTime: Date.now() / 1000,
            firstPaintAfterLoadTime: 0, navigationType: 'Other',
            wasFetchedViaSpdy: false, wasNpnNegotiated: false,
            npnNegotiatedProtocol: 'unknown', connectionInfo: 'http/1.1',
            wasAlternateProtocolAvailable: false
        })
    };

    // ── 4. 伪造 plugins ──
    Object.defineProperty(navigator, 'plugins', {
        get: () => {
            const PluginArray = function() {};
            PluginArray.prototype = Array.prototype;
            const arr = new PluginArray();
            arr.item = i => arr[i];
            arr.namedItem = n => arr.find(p => p.name === n);
            arr.refresh = () => {};
            arr.push(
                { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer',
                  description: 'Portable Document Format', length: 1,
                  0: { type: 'application/pdf', suffixes: 'pdf', description: 'Portable Document Format' } },
                { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                  description: '', length: 1,
                  0: { type: 'application/pdf', suffixes: 'pdf', description: '' } },
                { name: 'Native Client', filename: 'internal-nacl-plugin',
                  description: '', length: 2,
                  0: { type: 'application/x-nacl', suffixes: '', description: 'Native Client Executable' },
                  1: { type: 'application/x-pnacl', suffixes: '', description: 'Portable Native Client Executable' } }
            );
            return arr;
        }
    });

    // ── 5. 伪造 mimeTypes ──
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

    // ── 6. 伪造硬件信息 ──
    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
    Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 0 });

    // ── 7. 伪造语言/地区 ──
    Object.defineProperty(navigator, 'language', { get: () => 'zh-TW' });
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-TW', 'zh', 'en'] });
    Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });

    // ── 8. 伪造屏幕分辨率（常见 1920x1080） ──
    Object.defineProperty(screen, 'width', { get: () => 1920 });
    Object.defineProperty(screen, 'height', { get: () => 1080 });
    Object.defineProperty(screen, 'availWidth', { get: () => 1920 });
    Object.defineProperty(screen, 'availHeight', { get: () => 1040 });
    Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
    Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });

    // ── 9. 伪造 permissions.query ──
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

    // ── 10. 伪造 WebGL 指纹 ──
    const getParameterProxies = {
        [WebGLRenderingContext.prototype.VENDOR]: 'Google Inc. (Intel)',
        [WebGLRenderingContext.prototype.RENDERER]:
            'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
    };
    const origGetParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(p) {
        return getParameterProxies[p] || origGetParameter.call(this, p);
    };
    if (typeof WebGL2RenderingContext !== 'undefined') {
        const gp2 = {
            [WebGL2RenderingContext.prototype.VENDOR]: 'Google Inc. (Intel)',
            [WebGL2RenderingContext.prototype.RENDERER]:
                'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)'
        };
        const origGP2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(p) {
            return gp2[p] || origGP2.call(this, p);
        };
    }

    // ── 11. Canvas 指纹噪声 ──
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

    // ── 12. 伪造 performance.memory ──
    if (performance.memory === undefined) {
        Object.defineProperty(performance, 'memory', {
            get: () => ({
                jsHeapSizeLimit: 2172649472,
                totalJSHeapSize: 42000000,
                usedJSHeapSize: 38000000
            })
        });
    }

    // ── 13. 伪造 connection ──
    if (navigator.connection === undefined) {
        Object.defineProperty(navigator, 'connection', {
            get: () => ({
                effectiveType: '4g',
                rtt: 50,
                downlink: 10,
                saveData: false
            })
        });
    }

    // ── 14. 隐藏 headless 特征 ──
    Object.defineProperty(document, 'hidden', { get: () => false });
    Object.defineProperty(document, 'visibilityState', { get: () => 'visible' });

    // ── 15. reCAPTCHA 语言强制 zh-TW ──
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
    new MutationObserver(setRecaptchaLang).observe(document.body || document.documentElement,
        { childList: true, subtree: true });

    // ── 16. 拦截 window.open 以便外部感知 ──
    const _origOpen = window.open;
    window.open = function(url, target, features) {
        console.log('[Stealth] window.open intercepted:', url, target);
        // 仍然调用原始 open，但通过 console 日志让外部可追踪
        return _origOpen.call(window, url, target, features);
    };

    console.log('[Stealth] All anti-detection patches applied');
})();
"""


class BaseWebEngineView(QWebEngineView):
    """共享的浏览器引擎基类：无持久化存储、反检测 JS、Cookie 同步、页面跳转感知。

    每次创建实例都是全新的浏览器会话（off-the-record profile），
    不会保留任何本地缓存、Cookie 或存储。

    关键特性：
    - 每次页面加载完成自动注入反检测 JS（包括跳转后的新页面）
    - urlChanged 信号暴露，外部可监听页面跳转
    - 导航请求拦截，可阻止/放行特定 URL
    - Cookie 双向同步（浏览器 ↔ requests）
    """

    # ── 自定义信号 ──
    url_changed = Signal(str)          # URL 变化时发射（携带新 URL 字符串）
    title_changed = Signal(str)        # 标题变化时发射
    navigation_blocked = Signal(str)   # 导航被拦截时发射（携带被拦截的 URL）

    def __init__(self, parent=None):
        super().__init__(parent)

        # 使用 off-the-record profile：每次都是全新会话，无磁盘缓存
        self.profile = QWebEngineProfile(self)
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        )
        self.profile.setHttpAcceptLanguage("zh-TW,zh;q=0.9,en;q=0.8")

        self.custom_page = QWebEnginePage(self.profile, self)
        self.setPage(self.custom_page)

        # ── WebEngine 设置 ──
        settings = self.page().settings()
        attr = QWebEngineSettings.WebAttribute
        settings.setAttribute(attr.JavascriptEnabled, True)
        settings.setAttribute(attr.LocalStorageEnabled, True)
        settings.setAttribute(attr.AllowRunningInsecureContent, True)
        settings.setAttribute(attr.JavascriptCanAccessClipboard, True)
        settings.setAttribute(attr.AllowGeolocationOnInsecureOrigins, True)
        settings.setAttribute(attr.PlaybackRequiresUserGesture, False)
        settings.setAttribute(attr.WebGLEnabled, True)
        settings.setAttribute(attr.FocusOnNavigationEnabled, False)
        settings.setAttribute(attr.ErrorPageEnabled, False)
        settings.setAttribute(attr.FullScreenSupportEnabled, True)
        settings.setAttribute(attr.ScreenCaptureEnabled, True)
        settings.setAttribute(attr.AutoLoadImages, True)
        settings.setAttribute(attr.JavascriptCanOpenWindows, True)
        settings.setAttribute(attr.DnsPrefetchEnabled, True)

        # ── 内部状态 ──
        self.cookies = {}
        self._stealth_injected_urls = set()  # 记录已注入反检测 JS 的 URL
        self._navigation_history = []         # 导航历史 [(url, title), ...]
        self._current_history_index = -1
        self._blocked_url_patterns = []       # 要拦截的 URL 模式列表

        # ── 信号连接 ──
        self.profile.cookieStore().cookieAdded.connect(self._on_cookie_added)
        self.page().loadFinished.connect(self._on_load_finished)
        self.urlChanged.connect(self._on_url_changed)
        self.titleChanged.connect(self._on_title_changed)

    # ═══════════════════════════════════════════════════════════════
    # Cookie 管理
    # ═══════════════════════════════════════════════════════════════

    def _on_cookie_added(self, cookie):
        from src.config.GlobalConfig import GLOBAL_CONFIG
        key = cookie.name().data().decode("utf-8")
        value = cookie.value().data().decode("utf-8")
        domain = str(cookie.domain())
        self.cookies[(key, domain)] = value
        if key == "bfWebToken":
            GLOBAL_CONFIG.bf_web_token = value
            logging.info(f"[BaseWebEngine] bfWebToken 已捕获: {value[:20]}...")

    def sync_cookies_to_requests(self):
        """将浏览器 Cookie 同步到 requests 客户端"""
        from src.client import RequestClient
        try:
            jar = RequestClient.get_instance().client.cookies
            jar.clear()
            for (key, domain), value in self.cookies.items():
                secure = domain.endswith("beanfun.com") or domain.endswith("google.com")
                jar.set(
                    name=key, value=value, domain=domain, path="/",
                    secure=secure, expires=None, rest={}, version=0
                )
            logging.info(f"[BaseWebEngine] Cookie 已同步到 requests 客户端 ({len(self.cookies)} 条)")
        except Exception as e:
            logging.error(f"[BaseWebEngine] 同步 Cookie 失败: {e}")

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
            logging.info("[BaseWebEngine] Cookie 已从 requests 同步到浏览器")
        except Exception as e:
            logging.error(f"[BaseWebEngine] 同步 Cookie 到浏览器失败: {e}")

    # ═══════════════════════════════════════════════════════════════
    # 反检测 JS 注入（每次页面加载都注入）
    # ═══════════════════════════════════════════════════════════════

    def _on_load_finished(self, ok):
        """页面加载完成时注入反检测 JS。每次跳转后的新页面都会重新注入。"""
        if not ok:
            return
        current_url = self.url().toString()
        # 跳过空白页和 about: 页面
        if not current_url or current_url == "about:blank" or current_url.startswith("about:"):
            return
        # 每个新 URL 都注入（不再使用全局 _stealth_injected 标志）
        if current_url not in self._stealth_injected_urls:
            self._stealth_injected_urls.add(current_url)
            self.page().runJavaScript(STEALTH_JS)
            logging.debug(f"[BaseWebEngine] 反检测 JS 已注入: {current_url[:80]}")

    # ═══════════════════════════════════════════════════════════════
    # URL 变化追踪 & 导航历史
    # ═══════════════════════════════════════════════════════════════

    def _on_url_changed(self, url: QUrl):
        """内部 URL 变化处理：记录导航历史、发射自定义信号"""
        url_str = url.toString()
        if not url_str or url_str == "about:blank":
            return

        # 避免重复记录同一个 URL
        if (self._navigation_history and
                self._navigation_history[self._current_history_index][0] == url_str):
            return

        # 截断当前位置之后的历史（新导航会覆盖"前进"历史）
        if self._current_history_index < len(self._navigation_history) - 1:
            self._navigation_history = self._navigation_history[:self._current_history_index + 1]

        self._navigation_history.append((url_str, self.title()))
        self._current_history_index = len(self._navigation_history) - 1

        # 发射自定义信号
        self.url_changed.emit(url_str)
        logging.debug(f"[BaseWebEngine] URL 变更: {url_str[:100]}")

    def _on_title_changed(self, title: str):
        """内部标题变化处理"""
        if title and self._navigation_history:
            idx = self._current_history_index
            self._navigation_history[idx] = (self._navigation_history[idx][0], title)
        self.title_changed.emit(title)

    def current_url(self) -> str:
        """获取当前 URL 字符串"""
        return self.url().toString()

    def current_title(self) -> str:
        """获取当前页面标题"""
        return self.title()

    def get_navigation_history(self) -> list:
        """获取导航历史列表 [(url, title), ...]"""
        return list(self._navigation_history)

    def can_go_back_in_history(self) -> bool:
        """是否有更早的历史记录"""
        return self._current_history_index > 0

    def can_go_forward_in_history(self) -> bool:
        """是否有更新的历史记录"""
        return self._current_history_index < len(self._navigation_history) - 1

    # ═══════════════════════════════════════════════════════════════
    # 导航请求拦截
    # ═══════════════════════════════════════════════════════════════

    def add_blocked_url_pattern(self, pattern: str):
        """添加要拦截的 URL 模式（支持子串匹配）。

        示例:
            add_blocked_url_pattern("logout")
            add_blocked_url_pattern("exit.aspx")
        """
        if pattern not in self._blocked_url_patterns:
            self._blocked_url_patterns.append(pattern)
            logging.info(f"[BaseWebEngine] 已添加 URL 拦截模式: {pattern}")

    def remove_blocked_url_pattern(self, pattern: str):
        """移除 URL 拦截模式"""
        if pattern in self._blocked_url_patterns:
            self._blocked_url_patterns.remove(pattern)

    def acceptNavigationRequest(self, url: QUrl, nav_type, is_main_frame: bool) -> bool:
        """重写导航请求拦截。可在此阻止特定 URL 的跳转。

        返回 True 允许导航，False 阻止导航。
        """
        url_str = url.toString()

        # 检查拦截列表
        for pattern in self._blocked_url_patterns:
            if pattern in url_str:
                logging.info(f"[BaseWebEngine] 导航被拦截: {url_str[:100]} (匹配模式: {pattern})")
                self.navigation_blocked.emit(url_str)
                return False

        # 允许所有其他导航
        return True

    # ═══════════════════════════════════════════════════════════════
    # 弹窗 / 新窗口处理
    # ═══════════════════════════════════════════════════════════════

    def createWindow(self, windowType):
        """处理 window.open() 和 target="_blank" 的弹窗请求。

        策略：在当前视图中打开（模拟真实浏览器的"在当前标签页打开"行为），
        同时发射 url_changed 信号让外部感知跳转。
        """
        logging.info(f"[BaseWebEngine] createWindow 被调用, type={windowType}，将在当前视图打开")
        return self

    # ═══════════════════════════════════════════════════════════════
    # 便捷方法
    # ═══════════════════════════════════════════════════════════════

    def navigate(self, url: str):
        """导航到指定 URL"""
        if url.startswith(("http://", "https://")):
            self.load(QUrl(url))
        else:
            self.load(QUrl(f"https://{url}"))

    def reload_and_clear_stealth(self):
        """强制刷新并清除反检测注入记录（用于需要重新注入的场景）"""
        current = self.url().toString()
        self._stealth_injected_urls.discard(current)
        self.reload()

    def clear_state(self):
        """清除所有内部状态（Cookie、历史、注入记录）"""
        self.cookies.clear()
        self._stealth_injected_urls.clear()
        self._navigation_history.clear()
        self._current_history_index = -1
        logging.info("[BaseWebEngine] 内部状态已清除")
