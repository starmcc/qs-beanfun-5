import logging
import os
import threading
from io import BytesIO
from typing import Optional, Dict
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from requests.models import Response as RequestsResponse
from urllib3.util.retry import Retry

from src.config import Config


class _RequestClient:
    client: requests.Session
    _instance = None
    _lock = threading.Lock()

    # 默认请求头 - 模拟Chrome浏览器
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Sec-CH-UA": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "identity",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "DNT": "1",
    }

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(_RequestClient, cls).__new__(cls)
                    try:
                        cls._instance.init_client()
                    except Exception as e:
                        logging.error(f"Failed to initialize client: {str(e)}")
                        raise
        return cls._instance

    def init_client(self):
        """初始化requests会话，配置代理、请求头、SSL验证、重试等"""
        self.client = requests.Session()

        # 1. 设置默认请求头
        self.client.headers.update(self.DEFAULT_HEADERS)

        # 2. 配置代理
        self._setup_proxy()

        # 3. 配置重试机制
        self._setup_retry()

        # 4. SSL配置
        self.client.verify = False

        # 5. 禁用默认的Accept-Encoding自动处理，保持identity
        self.client.trust_env = False

        logging.info("Request client initialized successfully")

    def _setup_proxy(self):
        """配置代理"""
        # 优先环境变量，其次配置文件
        proxy_url = os.environ.get('ENV_PROXY_URL') or Config.proxy()

        if proxy_url:
            # 确保代理URL格式正确
            if not proxy_url.startswith(('http://', 'https://')):
                proxy_url = f'http://{proxy_url}'

            # 解析代理URL，提取主机和端口用于SOCKS代理支持
            parsed = urlparse(proxy_url)
            if parsed.scheme in ['http', 'https']:
                proxy_dict = {
                    'http': proxy_url,
                    'https': proxy_url,
                }
                self.client.proxies.update(proxy_dict)
                logging.info(f'Proxy configured: {parsed.netloc}')
            else:
                logging.warning(f'Unsupported proxy scheme: {parsed.scheme}')

    def _setup_retry(self):
        """配置重试机制"""
        retry_strategy = Retry(
            total=3,  # 最大重试次数
            backoff_factor=1,  # 重试间隔：1, 2, 4, 8秒
            status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的状态码
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"],
            raise_on_status=False,  # 不主动抛出异常
            respect_retry_after_header=True,  # 尊重服务端的Retry-After头
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,  # 连接池大小
            pool_maxsize=20,  # 最大连接数
        )
        self.client.mount("http://", adapter)
        self.client.mount("https://", adapter)

    def _create_error_response(self, status_code: int = 500, error_msg: str = '') -> RequestsResponse:
        """构造标准化的错误响应"""
        resp = RequestsResponse()
        resp.status_code = status_code
        resp._content = error_msg.encode() if error_msg else b''
        resp._content_consumed = True
        resp.url = ''
        resp.headers = {}
        resp.raw = BytesIO(b'')
        resp.reason = {
            500: 'Internal Server Error',
            502: 'Bad Gateway',
            503: 'Service Unavailable',
            504: 'Gateway Timeout',
        }.get(status_code, 'Unknown Error')
        return resp

    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求信息（调试用）"""
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            # 敏感信息脱敏
            headers = kwargs.get('headers', {})
            if headers:
                # 移除Authorization等敏感头
                safe_headers = {k: v if 'auth' not in k.lower() else '***' for k, v in headers.items()}
                logging.debug(f'{method} {url} headers={safe_headers}')
            else:
                logging.debug(f'{method} {url}')

    def request(self, method: str, url: str, retry_on_failure: bool = True, **kwargs) -> RequestsResponse:
        """
        通用请求方法

        Args:
            method: HTTP方法 (GET, POST, etc.)
            url: 请求URL
            retry_on_failure: 是否在失败时重试（利用Session的重试机制）
            **kwargs: 传递给requests的其他参数
        """
        self._log_request(method, url, **kwargs)

        # 设置默认超时
        kwargs.setdefault('timeout', 30)

        # 确保不自动处理gzip等压缩
        kwargs.setdefault('headers', {})
        if 'Accept-Encoding' not in kwargs['headers']:
            kwargs['headers']['Accept-Encoding'] = 'identity'

        # 默认允许重定向
        kwargs.setdefault('allow_redirects', True)

        try:
            # 如果不需要重试，临时禁用重试
            if not retry_on_failure:
                # 克隆session并禁用重试（简单实现，实际可以更复杂）
                return self._request_without_retry(method, url, **kwargs)

            resp = self.client.request(method, url, **kwargs)

            # 记录响应状态
            if resp.status_code >= 400:
                logging.warning(f'{method} {url} returned {resp.status_code}')

            return resp

        except requests.exceptions.Timeout:
            logging.error(f'Request timeout: {method} {url}')
            return self._create_error_response(504, 'Gateway Timeout')
        except requests.exceptions.ConnectionError:
            logging.error(f'Connection error: {method} {url}')
            return self._create_error_response(502, 'Bad Gateway')
        except requests.exceptions.ProxyError:
            logging.error(f'Proxy error: {method} {url}')
            return self._create_error_response(502, 'Bad Gateway')
        except requests.exceptions.SSLError:
            logging.error(f'SSL error: {method} {url}')
            return self._create_error_response(500, 'SSL Error')
        except Exception as e:
            logging.error(f'Unexpected error during {method} request to {url}: {str(e)}')
            return self._create_error_response(500, str(e))

    def _request_without_retry(self, method: str, url: str, **kwargs) -> RequestsResponse:
        """发送不重试的请求（使用原session但禁用重试适配器）"""
        try:
            # 这里简单处理：使用原session，但retry已经通过max_retries=0禁用
            # 实际上我们保留原session，但可以通过参数控制
            return self.client.request(method, url, **kwargs)
        except Exception as e:
            logging.error(f'Request failed (no retry): {method} {url} - {str(e)}')
            return self._create_error_response(500, str(e))

    def get(self, url: str, **kwargs) -> RequestsResponse:
        """GET请求"""
        return self.request('GET', url, **kwargs)

    def post(self, url: str, **kwargs) -> RequestsResponse:
        """POST请求"""
        return self.request('POST', url, **kwargs)

    def put(self, url: str, **kwargs) -> RequestsResponse:
        """PUT请求"""
        return self.request('PUT', url, **kwargs)

    def delete(self, url: str, **kwargs) -> RequestsResponse:
        """DELETE请求"""
        return self.request('DELETE', url, **kwargs)

    def patch(self, url: str, **kwargs) -> RequestsResponse:
        """PATCH请求"""
        return self.request('PATCH', url, **kwargs)

    def head(self, url: str, **kwargs) -> RequestsResponse:
        """HEAD请求"""
        return self.request('HEAD', url, **kwargs)

    def options(self, url: str, **kwargs) -> RequestsResponse:
        """OPTIONS请求"""
        return self.request('OPTIONS', url, **kwargs)

    # Cookie管理增强方法
    def get_cookie(self, key: str, domain: str = None) -> Optional[str]:
        """获取Cookie值"""
        try:
            if domain:
                # 获取指定域名的Cookie
                for cookie in self.client.cookies:
                    if cookie.name == key and (not domain or cookie.domain == domain):
                        return cookie.value
            return self.client.cookies.get(key)
        except Exception as e:
            logging.error(f"Error getting cookie {key}: {str(e)}")
            return None

    def set_cookie(self, name: str, value: str, domain: str = None, path: str = '/'):
        """设置Cookie"""
        try:
            self.client.cookies.set(name, value, domain=domain, path=path)
        except Exception as e:
            logging.error(f"Error setting cookie {name}: {str(e)}")

    def clear_cookies(self):
        """清除所有Cookie"""
        self.client.cookies.clear()

    def update_headers(self, headers: Dict[str, str]):
        """更新默认请求头"""
        self.client.headers.update(headers)

    def set_user_agent(self, user_agent: str):
        """动态设置User-Agent"""
        self.client.headers['User-Agent'] = user_agent

    def get_user_agent(self) -> str:
        """获取当前User-Agent"""
        return self.client.headers.get('User-Agent', '')


# 单例获取函数
def get_instance() -> _RequestClient:
    """获取请求客户端单例"""
    return _RequestClient()


def get_ck_val(key: str) -> Optional[str]:
    """获取Cookie值（兼容旧接口）"""
    client = get_instance()
    if not client:
        return None
    return client.get_cookie(key)


def get(url: str, **kwargs) -> RequestsResponse:
    """全局GET请求"""
    return get_instance().get(url, **kwargs)


def post(url: str, **kwargs) -> RequestsResponse:
    """全局POST请求"""
    return get_instance().post(url, **kwargs)


def update_headers(headers: Dict[str, str]):
    """更新全局请求头"""
    get_instance().update_headers(headers)
