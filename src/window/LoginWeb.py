import logging
import os
import tempfile

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

    def sync_requests_cookies(self):
        try:
            # 1. 获取 requests 的 CookieJar
            cookies_jar = RequestClient.get_instance().client.cookies
            # 2. 清空原有 Cookie
            cookies_jar.clear()

            # 3. 遍历本地 Cookie 字典，同步到 requests 的 CookieJar
            for (key, domain), value in self.cookies.items():
                # 使用 requests CookieJar 的 set 方法添加 Cookie
                cookies_jar.set(
                    name=key,  # Cookie 名称
                    value=value,  # Cookie 值
                    domain=domain,  # Cookie 域名
                    path="/",  # Cookie 路径
                    secure=False,  # 是否仅 HTTPS 生效
                    expires=None,  # 过期时间
                    rest={},  # 其他扩展属性
                    version=0  # Cookie 版本
                )
            logging.info("Cookie 已成功同步到 requests 客户端")
        except Exception as e:
            logging.error(f"同步 Cookie 到 requests 时出错: {str(e)}")

    def clear_all_data(self):
        self.cookies.clear()  # 清除内存Cookie
        self.profile.cookieStore().deleteAllCookies()  # 清除Profile中的Cookie
        self.profile.clearAllVisitedLinks()  # 清除访问记录
        
        if hasattr(self, 'temp_dir') and self.temp_dir:
            try:
                # 先停止所有WebEngine活动
                self.stop()
                self.load(QUrl("about:blank"))  # 加载空白页面释放资源
                
                # 更安全的清理策略
                import threading
                import shutil
                import os
                
                def safe_cleanup():
                    import time
                    time.sleep(2)  # 等待2秒确保资源释放
                    
                    try:
                        # 尝试标准清理
                        self.temp_dir.cleanup()
                    except Exception as e:
                        # 如果标准清理失败，尝试手动清理
                        logging.warning(f"标准清理失败，尝试手动清理: {str(e)}")
                        try:
                            temp_path = self.temp_dir.name
                            if os.path.exists(temp_path):
                                # 使用更安全的清理方法
                                shutil.rmtree(temp_path, ignore_errors=True)
                        except Exception as e2:
                            # 如果手动清理也失败，记录警告但继续
                            logging.warning(f"手动清理也失败，临时目录可能残留: {str(e2)}")
                
                # 在后台线程中执行清理
                cleanup_thread = threading.Thread(target=safe_cleanup)
                cleanup_thread.daemon = True
                cleanup_thread.start()
                
            except Exception as e:
                logging.warning(f"清理临时文件时出现警告: {str(e)}")


class LoginWeb(QDialog):
    _instance = None

    def __init__(self, parent):
        if LoginWeb._instance is not None:
            raise Exception("LoginWeb窗口只能打开一个")
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
        self.enter_btn = QPushButton(WinManager.translate("确认登入状态(请成功登入后点击此处)"))
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

    def on_login_enter(self, event=None):
        if GLOBAL_CONFIG.bf_web_token:
            self.web_view.sync_requests_cookies()
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
            loop.exec_()
            
            # 检查响应状态
            if reply.error() == QNetworkReply.NoError:
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
            # 网络管理器会自动被Qt的父子关系管理清理

    def closeEvent(self, event: QCloseEvent):
        """安全关闭窗口，确保资源正确释放"""
        if hasattr(self, 'web_view'):
            # 先停止WebEngine活动
            self.web_view.stop()
            # 加载空白页面释放资源
            self.web_view.load(QUrl("about:blank"))
            # 异步清理数据
            self.web_view.clear_all_data()
            # 延迟删除视图
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
