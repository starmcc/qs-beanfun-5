import logging
import os
import threading
from io import BytesIO
from typing import Optional

import requests
from requests.models import Response as RequestsResponse

from src.config import Config


class _RequestClient:
    client: requests.Session  # 替换为requests的会话对象
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """保持原有的线程安全单例模式"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(_RequestClient, cls).__new__(cls)
                    try:
                        cls._instance.init_client()
                    except Exception as e:
                        logging.error(f"Failed to initialize client: {str(e)}")
        return cls._instance

    def init_client(self):
        """初始化requests会话，配置代理、请求头、SSL验证等"""
        # 代理配置：优先环境变量，其次配置文件
        proxies = os.environ.get('ENV_PROXY_URL')
        if not proxies:
            proxies = Config.proxy()

        # 构建代理字典（requests要求指定http/https协议）
        proxy_dict = {}
        if proxies:
            logging.info(f'use proxy {proxies}')
            proxy_dict = {
                'http': proxies,
                'https': proxies
            }

        # 请求头配置
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Accept-Encoding": "identity",
            "Connection": "Keep-Alive",
        }

        # 初始化requests会话
        self.client = requests.Session()
        self.client.headers.update(headers)  # 设置会话默认请求头
        self.client.proxies = proxy_dict  # 设置代理
        self.client.verify = False  # 禁用SSL证书验证

    def _create_error_response(self, status_code: int = 500) -> RequestsResponse:
        """构造自定义错误响应"""
        resp = RequestsResponse()
        resp.status_code = status_code
        resp._content = b''  # 响应体为空
        resp._content_consumed = True  # 标记内容已消费
        resp.url = ''
        resp.headers = {}
        resp.raw = BytesIO(b'')  # 原始响应流
        resp.reason = 'Internal Server Error' if status_code == 500 else ''
        return resp

    def get(self, url: str, **kwargs) -> RequestsResponse:
        """GET请求封装，异常时返回500响应"""
        try:
            kwargs.setdefault('timeout', 10)
            resp = self.client.get(url, **kwargs)
            # requests默认allow_redirects=True
            return resp
        except Exception as e:
            logging.error(f"Unexpected error during GET request to {url}: {str(e)}")
            return self._create_error_response(500)

    def post(self, url: str, **kwargs) -> RequestsResponse:
        """POST请求封装，异常时返回500响应"""
        try:
            kwargs.setdefault('timeout', 10)
            resp = self.client.post(url, **kwargs)
            return resp
        except Exception as e:
            logging.error(f"Unexpected error during POST request to {url}: {str(e)}")
            return self._create_error_response(500)


def get_instance() -> _RequestClient:
    """获取请求客户端单例"""
    return _RequestClient()


def get_ck_val(key: str) -> Optional[str]:
    client = get_instance()
    if not client:
        return None
    try:
        # requests的CookieJar直接通过get方法获取值
        return client.client.cookies.get(key)
    except Exception as e:
        logging.error(f"Error getting cookie value: {str(e)}")
        return None
