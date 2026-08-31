"""
GithubHostsProxy 模块
=====================
本地 HTTP 代理服务器，根据 github-hosts 的「域名 -> IP」映射解析域名，
实现不修改系统 hosts 文件即可直连 GitHub 的效果。

支持：
  - HTTP 请求转发
  - HTTPS CONNECT 隧道（建立到目标 IP 的连接后透传加密流量）
"""
import logging
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, Optional

from src.client.updater.GithubHosts import fetch_hosts

# 默认监听地址和端口
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 7899


class _ProxyHandler(BaseHTTPRequestHandler):
    """HTTP 代理请求处理器"""

    # 关闭默认的日志输出（避免刷屏）
    def log_message(self, format, *args):
        pass

    def _resolve_host(self, host: str) -> str:
        """根据 hosts 映射解析域名，返回目标 IP"""
        # 去掉端口
        hostname = host.split(':')[0]
        ip = self.server.hosts_map.get(hostname)
        if ip:
            logging.debug(f"hosts 命中: {hostname} -> {ip}")
            return ip
        return hostname

    def do_CONNECT(self):
        """处理 HTTPS CONNECT 隧道"""
        host, _, port = self.path.partition(':')
        port = int(port) if port else 443
        target_ip = self._resolve_host(host)

        try:
            # 建立到目标 IP 的连接
            remote = socket.create_connection((target_ip, port), timeout=30)
            self.send_response(200, "Connection Established")
            self.end_headers()

            # 双向透传加密流量
            self._tunnel(self.connection, remote)
        except Exception as e:
            logging.error(f"CONNECT 隧道建立失败 {host}:{port} -> {target_ip}: {str(e)}")
            try:
                self.send_error(502, "Bad Gateway")
            except Exception:
                pass

    def do_GET(self):
        self._forward_http()

    def do_POST(self):
        self._forward_http()

    def do_PUT(self):
        self._forward_http()

    def do_DELETE(self):
        self._forward_http()

    def do_HEAD(self):
        self._forward_http()

    def do_OPTIONS(self):
        self._forward_http()

    def _forward_http(self):
        """转发普通 HTTP 请求"""
        try:
            # 解析目标地址（代理请求格式: http://host:port/path）
            url = self.path
            if url.startswith('http://'):
                rest = url[len('http://'):]
                host_port, _, path = rest.partition('/')
                path = '/' + path
            else:
                host_port = self.headers.get('Host', '')
                path = url

            host, _, port = host_port.partition(':')
            port = int(port) if port else 80
            target_ip = self._resolve_host(host)

            # 建立到目标 IP 的连接
            remote = socket.create_connection((target_ip, port), timeout=30)

            # 构造转发请求
            request_line = f"{self.command} {path} HTTP/1.1\r\n"
            headers = ""
            for key, value in self.headers.items():
                if key.lower() == 'proxy-connection':
                    continue
                headers += f"{key}: {value}\r\n"
            # 确保 Host 头保留原始域名（用于虚拟主机和 HTTPS 证书）
            if not any(k.lower() == 'host' for k in self.headers.keys()):
                headers += f"Host: {host_port}\r\n"

            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0) or 0)
            body = self.rfile.read(content_length) if content_length > 0 else b''

            remote.sendall(request_line.encode() + headers.encode() + "\r\n".encode() + body)

            # 转发响应
            self._relay_response(remote)
        except Exception as e:
            logging.error(f"HTTP 转发失败: {str(e)}")
            try:
                self.send_error(502, "Bad Gateway")
            except Exception:
                pass

    def _relay_response(self, remote: socket.socket):
        """将远程响应转发给客户端"""
        try:
            # 读取响应头
            response = b''
            while b'\r\n\r\n' not in response:
                chunk = remote.recv(4096)
                if not chunk:
                    break
                response += chunk

            # 解析 Content-Length 或 chunked
            header_part, _, body_part = response.partition(b'\r\n\r\n')
            headers_text = header_part.decode('latin-1', errors='ignore')

            # 发送响应头
            self.connection.sendall(header_part + b'\r\n\r\n')

            # 处理响应体
            if 'Transfer-Encoding: chunked' in headers_text:
                # chunked 编码，直接透传
                self.connection.sendall(body_part)
                while True:
                    chunk = remote.recv(4096)
                    if not chunk:
                        break
                    self.connection.sendall(chunk)
            else:
                # 根据 Content-Length 读取
                content_length = 0
                for line in headers_text.split('\r\n'):
                    if line.lower().startswith('content-length:'):
                        content_length = int(line.split(':', 1)[1].strip())
                        break

                # 发送已读取的 body 部分
                self.connection.sendall(body_part)
                remaining = content_length - len(body_part)
                while remaining > 0:
                    chunk = remote.recv(min(4096, remaining))
                    if not chunk:
                        break
                    self.connection.sendall(chunk)
                    remaining -= len(chunk)
        except Exception as e:
            logging.error(f"响应转发失败: {str(e)}")
        finally:
            try:
                remote.close()
            except Exception:
                pass

    def _tunnel(self, client: socket.socket, remote: socket.socket):
        """双向透传（用于 HTTPS CONNECT 隧道）"""
        def pipe(src, dst):
            try:
                while True:
                    data = src.recv(4096)
                    if not data:
                        break
                    dst.sendall(data)
            except Exception:
                pass
            finally:
                try:
                    dst.shutdown(socket.SHUT_WR)
                except Exception:
                    pass

        t1 = threading.Thread(target=pipe, args=(client, remote), daemon=True)
        t2 = threading.Thread(target=pipe, args=(remote, client), daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


class GithubHostsProxy:
    """github-hosts 本地代理管理器"""

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.hosts_map: Dict[str, str] = {}
        self._server: Optional[ThreadingHTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    def start(self) -> bool:
        """
        启动代理服务器。

        先获取 github-hosts 映射，再启动本地代理。
        返回是否启动成功。
        """
        # 获取 hosts 映射
        self.hosts_map = fetch_hosts()
        if not self.hosts_map:
            logging.warning("未获取到 github-hosts 映射，代理无法提供 hosts 解析")
            return False

        try:
            # 创建代理服务器，注入 hosts_map
            server = ThreadingHTTPServer((self.host, self.port), _ProxyHandler)
            server.hosts_map = self.hosts_map
            self._server = server

            # 后台线程运行
            self._thread = threading.Thread(target=server.serve_forever, daemon=True)
            self._thread.start()

            logging.info(f"github-hosts 代理已启动: http://{self.host}:{self.port}")
            return True
        except Exception as e:
            logging.error(f"启动 github-hosts 代理失败: {str(e)}")
            return False

    def stop(self):
        """停止代理服务器"""
        if self._server:
            try:
                self._server.shutdown()
                self._server.server_close()
            except Exception as e:
                logging.error(f"停止代理失败: {str(e)}")
            self._server = None

    @property
    def proxy_url(self) -> str:
        """获取代理地址"""
        return f"http://{self.host}:{self.port}"


# 全局单例
_instance: Optional[GithubHostsProxy] = None


def get_instance() -> GithubHostsProxy:
    """获取代理单例"""
    global _instance
    if _instance is None:
        _instance = GithubHostsProxy()
    return _instance
