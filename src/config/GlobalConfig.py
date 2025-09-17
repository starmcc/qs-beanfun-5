# 加载 UI 文件
from enum import Enum

from src.utils.TaskQueue import TaskQueue


class ActType(Enum):
    """类型枚举"""
    HK = "HK"  # 香港地区
    TW = "TW"  # 台湾地区


class GlobalConstants:
    """全局常量集中管理"""
    APP_VERSION = "5.3.0"
    GITHUB_URL = "https://github.com/starmcc/qs-beanfun-5"
    GITHUB_API_URL = "https://api.github.com/repos/starmcc/qs-beanfun-5"


class _GlobalConfig:
    """全局配置单例类，管理应用程序全局状态"""
    _instance = None  # 单例实例

    def __new__(cls, *args, **kwargs):
        """实现单例模式，确保全局只有一个实例"""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # 防止重复初始化（单例模式必要处理）
        if hasattr(self, "_initialized"):
            return

        self.bf_web_token: str = ""
        self.win_main = None
        self.win_actManager = None
        self.win_config = None
        self.win_accountInfo = None
        self.win_about = None
        self.win_nav = None
        self.win_twAdv = None
        self.win_intermediateLogin = None
        self.win_qrCode = None

        # 任务队列
        self.custom_queue = TaskQueue()

        self.now_login_type: str = ""

        self._initialized = True  # 标记初始化完成


# 全局配置实例（单例）
GLOBAL_CONFIG = _GlobalConfig()
