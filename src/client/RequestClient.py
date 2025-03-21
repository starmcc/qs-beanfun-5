import logging
import os
import threading
import httpx


class _RequestClient:
    client: httpx.Client
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(_RequestClient, cls).__new__(cls)
                    try:
                        cls._instance.init_client()
                    except Exception as e:
                        logging.error(f"Failed to initialize client: {e}")
        return cls._instance

    def init_client(self):
        proxies = os.environ.get('ENV_PROXY_URL')
        if proxies:
            logging.info(f'use proxy {proxies}')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Accept-Encoding": "identity",
            "Connection": "Keep-Alive",
        }
        try:
            self.client = httpx.Client(follow_redirects=True,
                                       verify=False,
                                       proxies=proxies,
                                       headers=headers,
                                       timeout=30)
        except httpx.RequestError as req_err:
            logging.error(f"Error creating HTTP client: {req_err}")
        except Exception as e:
            logging.error(f"Unexpected error while creating client: {e}")

    def get(self, url, **kwargs):
        try:
            return self.client.get(url, **kwargs)
        except httpx.RequestError as req_err:
            logging.error(f"Error occurred during GET request to {url}: {req_err}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during GET request to {url}: {e}")
            return None

    def post(self, url, **kwargs):
        try:
            return self.client.post(url, **kwargs)
        except httpx.RequestError as req_err:
            logging.error(f"Error occurred during POST request to {url}: {req_err}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during POST request to {url}: {e}")
            return None


def get_instance() -> _RequestClient:
    try:
        return _RequestClient()
    except Exception as e:
        logging.error(f"Error getting client instance: {e}")
        return None


def get_ck_val(key) -> str or None:
    client = get_instance()
    if client:
        try:
            cookies = client.client.cookies
            for cookie in cookies.jar:
                if cookie.name == key:
                    return cookie.value
        except Exception as e:
            logging.error(f"Error getting cookie value: {e}")
    return None


def get_cookies() -> list or None:
    client = get_instance()
    if client:
        try:
            cookie_list = []
            cookies = client.client.cookies
            for cookie in cookies.jar:
                cookie_list.append((cookie.name, cookie.value))
            return cookie_list
        except Exception as e:
            logging.error(f"Error getting cookies: {e}")
    return None
