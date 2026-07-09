# src/window/RecaptchaWeb.py
import logging
import tempfile
from pathlib import Path

from PySide6.QtCore import QEventLoop, QTimer, QUrl, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QDialog, QVBoxLayout

WEBVIEW_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
)

START_URL = "https://tw.beanfun.com/beanfun_block/bflogin/default.aspx?service=999999_T0"

RECAPTCHA_INIT_SCRIPT = r"""
(() => {
  'use strict';
  try { Object.defineProperty(navigator, 'webdriver', { get: () => false }); } catch (e) {}
  const OVERLAY_Z = 999999; // MUST stay below reCAPTCHA's challenge bframe (~2e9)
  const onReady = () => {
    if (location.href.indexOf('Login/Index') === -1) return;
    console.log('[reCAPTCHA] on Login/Index, watching for token');
    if (document.getElementById('__ov')) return;
    const style = document.createElement('style');
    style.textContent =
      '#__ov{position:fixed;inset:0;z-index:' + OVERLAY_Z + ';background:#1c1712;' +
      'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;' +
      'color:#f4ede4;font-family:system-ui,sans-serif;font-size:14px}' +
      '#__sp{width:34px;height:34px;border-radius:50%;border:3px solid rgba(244,237,228,.25);' +
      'border-top-color:#ff8201;animation:__r .8s linear infinite}' +
      '@keyframes __r{to{transform:rotate(360deg)}}' +
      '.grecaptcha-badge{z-index:' + (OVERLAY_Z + 1) + ' !important}';
    const ov = document.createElement('div'); ov.id = '__ov';
    const sp = document.createElement('div'); sp.id = '__sp';
    const lb = document.createElement('div'); lb.textContent = '驗證載入中，請稍候…';
    ov.appendChild(sp); ov.appendChild(lb);
    (document.head || document.documentElement).appendChild(style);
    (document.body || document.documentElement).appendChild(ov);
    const anchor = () =>
      document.querySelector("iframe[src*='recaptcha'][src*='anchor']") ||
      document.querySelector("iframe[title='reCAPTCHA']") ||
      document.querySelector("iframe[src*='recaptcha']");
    const findWidget = () => {
      const a = anchor(); if (!a) return null;
      let w = a.closest('.g-recaptcha');
      if (!w) {
        w = a;
        for (let i = 0; i < 5 && w.parentElement && w.parentElement !== document.body; i++) {
          w = w.parentElement;
          if (w.offsetWidth >= 280 && w.offsetWidth <= 400) break;
        }
      }
      return w;
    };
    let store = null;
    try { store = window.sessionStorage; } catch (e) {}
    const RKEY = '__rc_reloads__';
    let placed = false;
    const place = () => {
      if (placed) return;
      const w = findWidget();
      if (w && w !== document.body && w !== document.documentElement) {
        placed = true; clearInterval(rt);
        w.style.position = 'relative';
        w.style.zIndex = String(OVERLAY_Z + 2);
        sp.remove();
        lb.textContent = '請完成「我不是機器人」驗證';
        ov.appendChild(w); // reparent → iframe reload → fresh checkbox
        return;
      }
      // Safety-net path (no widget yet). Only give up once the reload has run.
      if (store && store.getItem(RKEY)) {
        placed = true; clearInterval(rt);
        try { store.removeItem(RKEY); } catch (e) {}
        console.warn('[reCAPTCHA] widget did not render (reload budget spent) — closing');
        if (window.__TAURI_INTERNALS__) {
          window.__TAURI_INTERNALS__.invoke('close_recaptcha_window').catch(() => {});
        }
      }
    };
    const rt = setInterval(() => { if (anchor()) place(); }, 200);
    setTimeout(place, 6000); // safety net so the spinner never sticks forever
    setTimeout(() => {
      if (!document.querySelector("iframe[src*='recaptcha']") && store && !store.getItem(RKEY)) {
        store.setItem(RKEY, '1');
        console.warn('[reCAPTCHA] widget did not render — reloading once');
        location.reload();
      }
    }, 4000);
    const readToken = () => {
      try {
        const g = window.grecaptcha;
        if (g && g.enterprise && typeof g.enterprise.getResponse === 'function') {
          const t = g.enterprise.getResponse();
          if (t) return t;
        }
        if (g && typeof g.getResponse === 'function') {
          const t = g.getResponse();
          if (t) return t;
        }
      } catch (e) {}
      const el = document.getElementById('recaptcha-token') ||
        document.querySelector('#g-recaptcha-response, textarea[name="g-recaptcha-response"]');
      return el ? el.value : '';
    };
    const initial = readToken();
    let done = false;
    const timer = setInterval(() => {
      if (done) return;
      const val = readToken();
      if (val && val !== initial && val.length > 50) {
        done = true;
        clearInterval(timer);
        if (store) { try { store.removeItem(RKEY); } catch (e) {} }
        const step = window.__RECAPTCHA_STEP__ || 'login';
        try { window.location.hash = 'mltoken=' + step + '~' + val; } catch (e) {}
        try {
          if (window.__TAURI_INTERNALS__) {
            window.__TAURI_INTERNALS__
              .invoke('submit_login_token', { token: val, step })
              .catch(() => {});
          }
        } catch (e) {}
        console.log('[reCAPTCHA] token captured, handed to backend via fragment');
      }
    }, 500);
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onReady, { once: true });
  } else {
    onReady();
  }
})();
"""


class RecaptchaWindow(QDialog):
    token_ready = Signal(str)
    cancelled = Signal()

    def __init__(self, step: str, parent=None):
        super().__init__(parent)
        self.step = step or "login"
        self._token_received = False
        self._data_dir = Path(tempfile.mkdtemp(prefix="qsbeanfun-recaptcha-"))

        self.setWindowTitle(f"請完成 reCAPTCHA 驗證 ({self.step})")
        self.resize(400, 550)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.profile = QWebEngineProfile(self)
        self.profile.setPersistentStoragePath(str(self._data_dir))
        self.profile.setCachePath(str(self._data_dir / "cache"))
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        self.profile.setHttpUserAgent(WEBVIEW_USER_AGENT)
        self.profile.setHttpAcceptLanguage("zh-TW,zh;q=0.9,en;q=0.8")

        self.page = QWebEnginePage(self.profile, self)
        self.browser = QWebEngineView(self)
        self.browser.setPage(self.page)
        layout.addWidget(self.browser)

        self._configure_settings()

        self.page.loadFinished.connect(self.on_load_finished)
        self.browser.urlChanged.connect(self.on_url_changed)

        self.browser.setUrl(QUrl(START_URL))

    def _configure_settings(self):
        settings = self.page.settings()
        attr = QWebEngineSettings.WebAttribute
        settings.setAttribute(attr.JavascriptEnabled, True)
        settings.setAttribute(attr.LocalStorageEnabled, True)
        settings.setAttribute(attr.JavascriptCanOpenWindows, True)
        settings.setAttribute(attr.AutoLoadImages, True)
        settings.setAttribute(attr.WebGLEnabled, True)
        settings.setAttribute(attr.PlaybackRequiresUserGesture, False)
        settings.setAttribute(attr.FullScreenSupportEnabled, True)
        settings.setAttribute(attr.ScreenCaptureEnabled, True)
        settings.setAttribute(attr.AllowRunningInsecureContent, True)
        settings.setAttribute(attr.FocusOnNavigationEnabled, False)
        settings.setAttribute(attr.ErrorPageEnabled, False)

    def on_load_finished(self, ok: bool):
        if not ok:
            logging.warning("[RecaptchaWindow] 页面加载失败")
            self.cancelled.emit()
            self.reject()
            return

        current_url = self.browser.url().toString()
        if "beanfun.com" not in current_url:
            return

        prelude = f"window.__RECAPTCHA_STEP__ = {self.step!r};\n"
        self.page.runJavaScript(prelude + RECAPTCHA_INIT_SCRIPT)
        logging.info(f"[RecaptchaWindow] 已注入脚本: {current_url[:120]}")

    def on_url_changed(self, url: QUrl):
        fragment = url.fragment()
        if not fragment.startswith("mltoken="):
            return

        payload = fragment[len("mltoken="):]
        if "~" not in payload:
            return

        step, token = payload.split("~", 1)
        if step != self.step:
            logging.info(f"[RecaptchaWindow] 忽略其他阶段 token: {step}")
            return

        if token and len(token) > 10:
            logging.info(f"[RecaptchaWindow] 捕获到 token，长度={len(token)}")
            self.on_token_received(token)

    def on_token_received(self, token: str):
        if token and not self._token_received:
            self._token_received = True
            self.token_ready.emit(token)
            self.accept()

    def closeEvent(self, event: QCloseEvent):
        if not self._token_received:
            self.cancelled.emit()
        super().closeEvent(event)
        self._cleanup_profile_dir()

    def _cleanup_profile_dir(self):
        try:
            if self.page is not None:
                self.page.setInspectedPage(None)
        except Exception:
            pass
        try:
            if self.profile is not None:
                self.profile.deleteLater()
        except Exception:
            pass
        QTimer.singleShot(1500, self._remove_profile_dir)

    def _remove_profile_dir(self):
        try:
            import shutil
            shutil.rmtree(self._data_dir, ignore_errors=True)
        except Exception as e:
            logging.warning(f"[RecaptchaWindow] 清理临时目录失败: {e}")


def get_recaptcha_token_sync(parent, step: str, timeout_ms: int = 180000) -> str | None:
    loop = QEventLoop()
    win = RecaptchaWindow(step, parent)
    token = None

    def on_token(t):
        nonlocal token
        token = t
        loop.quit()

    def on_cancelled():
        loop.quit()

    win.token_ready.connect(on_token)
    win.cancelled.connect(on_cancelled)
    win.finished.connect(lambda: loop.quit())

    win.show()
    loop.exec()
    return token
