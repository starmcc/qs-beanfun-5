# 加载 UI 文件
from src.utils.TaskQueue import TaskQueue
from src.window import LoadMask


class _GlobalConfig:
    mask: LoadMask

    def __init__(self):
        self.bf_web_token: str
        self.win_main = None
        self.win_browser = None
        self.win_actManager = None
        self.win_config = None
        self.win_accountInfo = None
        self.win_about = None
        self.win_twAdv = None
        self.win_intermediateLogin = None
        self.win_qrCode = None
        self.custom_thread = None
        self.custom_queue = TaskQueue()
        self.now_login_type = ''
        self.github_url = '5.0.1'


GLOBAL_CONFIG = _GlobalConfig()

GLOBAL_ACT_TYPE_HK = 'HK'
GLOBAL_ACT_TYPE_TW = 'TW'

GLOBAL_PATH_PLUGIN_LR_ZIP = 'LocaleRemulator.zip'
GLOBAL_PATH_PLUGIN_ZWW_ZIP = 'MapleNecrocer.zip'

GLOBAL_APP_VERSION = '4.0'

GLOBAL_APP_GITHUB = "https://github.com/starmcc/qs-beanfun-5"

GLOBAL_APP_GITHUB_API = "https://api.github.com/repos/starmcc/qs-beanfun-5"