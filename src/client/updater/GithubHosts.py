"""
GithubHosts 模块
================
从开源项目 https://github.com/maxiaof/github-hosts 获取 hosts 文件，
解析出「域名 -> IP」的映射关系，供本地代理使用，无需修改系统 hosts 文件。
"""
import base64
import logging
import re
from typing import Dict

import requests

# github-hosts 项目的 hosts 文件地址（通过 GitHub API 获取）
GITHUB_HOSTS_URL = "https://api.github.com/repos/maxiaof/github-hosts/contents/hosts"

# hosts 文件中的标记行，用于识别有效区间
HOSTS_START_MARK = "#Github Hosts Start"
HOSTS_END_MARK = "#Github Hosts End"


def fetch_hosts() -> Dict[str, str]:
    """
    获取 github-hosts 的 hosts 文件并解析为「域名 -> IP」映射。

    Returns:
        Dict[str, str]: 例如 {"github.com": "140.82.116.3", "api.github.com": "20.29.134.17"}
        获取或解析失败时返回空字典。
    """
    try:
        response = requests.get(GITHUB_HOSTS_URL, timeout=20)
        if response.status_code != 200:
            logging.warning(f"获取 github-hosts 失败，状态码: {response.status_code}")
            return {}

        # GitHub API 返回 JSON，content 字段为 Base64 编码的文件内容
        data = response.json()
        content = base64.b64decode(data.get('content', '')).decode('utf-8')
        return parse_hosts(content)
    except Exception as e:
        logging.error(f"获取 github-hosts 出现错误: {str(e)}")
        return {}


def parse_hosts(content: str) -> Dict[str, str]:
    """
    解析 hosts 文件内容，提取「域名 -> IP」映射。

    支持两种格式：
      1. 标准 hosts 行：`IP 域名`（如 `140.82.116.3 github.com`）
      2. 带 #Github Hosts Start/End 标记的区间

    Args:
        content: hosts 文件内容

    Returns:
        Dict[str, str]: 域名 -> IP 映射
    """
    hosts_map: Dict[str, str] = {}

    # 如果存在标记区间，只解析区间内的内容
    if HOSTS_START_MARK in content and HOSTS_END_MARK in content:
        start = content.index(HOSTS_START_MARK)
        end = content.index(HOSTS_END_MARK)
        content = content[start:end]

    # 匹配 hosts 行：IP 域名（忽略注释行和空行）
    # 支持 IPv4 和 IPv6
    pattern = re.compile(r'^\s*([0-9a-fA-F.:]+)\s+([a-zA-Z0-9.\-]+)\s*$', re.MULTILINE)
    for match in pattern.finditer(content):
        ip, domain = match.group(1), match.group(2)
        # 跳过 localhost 等特殊条目
        if domain in ('localhost', 'localhost.localdomain'):
            continue
        hosts_map[domain] = ip

    logging.info(f"解析 github-hosts 完成，共 {len(hosts_map)} 条映射")
    return hosts_map
