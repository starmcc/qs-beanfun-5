# 加载 UI 文件
from enum import Enum

from src.utils.TaskQueue import TaskQueue
from src.utils.GgmTableGenerate import decrypt_ggm_tables


class ActType(Enum):
    """类型枚举"""
    HK = "HK"  # 香港地区
    TW = "TW"  # 台湾地区

class LANGUAGE(Enum):
    ZH_CN = "zh_CN"
    ZH_TW = "zh_TW"
    EN = "en"

class GlobalConstants:
    """全局常量集中管理"""
    APP_VERSION = "5.7.8"
    GITHUB_URL = "https://github.com/starmcc/qs-beanfun-5"
    GITHUB_API_URL = "https://api.github.com/repos/starmcc/qs-beanfun-5"
    NAV_API_URL = "https://gitee.com/starmcc/qs-beanfun-nav/raw/master/config.json"


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
        self.win_double_code_input = None
        self.win_gamapass = None

        # 任务队列
        self.custom_queue = TaskQueue()

        self.now_login_type: str = ""
        # 标记是否使用 GamaPass 登录（仅台湾）
        self.is_gamapass_login: bool = False

        self._initialized = True  # 标记初始化完成

        # GGM DecryptParam 替换表（由 GgmTableGenerate 解密生成）共 8 个表。
        self.ggm = {
            'tables': decrypt_ggm_tables(),
            # https://tw.beanfun.com/generic_handlers/CheckVersion.ashx
            # GGMWebStart.dll 的 SHA-256（小写 hex），1.5.0.2 版本的固定 Hash
            'cv': '1.5.0.2',
            'dll_hash': 'dfd568a69d87abcd8f4a93d1a4481ebb57712d1d28ab0b6fc018fcf140101e06',
        }


# 全局配置实例（单例）
GLOBAL_CONFIG = _GlobalConfig()
