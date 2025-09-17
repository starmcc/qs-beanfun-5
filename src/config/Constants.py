from decimal import Decimal

class AppConstants:
    # 应用信息
    APP_VERSION = "5.3.0"
    GITHUB_URL = "https://github.com/starmcc/qs-beanfun-5"
    GITHUB_API_URL = "https://api.github.com/repos/starmcc/qs-beanfun-5"


class ConfigKeys:
    # 配置文件键名集中管理
    PASS_INPUT = "pass_input"
    STOP_UPDATE = "stop_update"
    CLOSE_START_WINDOW = "close_start_window"
    GAME_PATH = "game_path"
    AUTO_INPUT = "auto_input"
    UPDATE_TIPS_TIME = "update_tips_time"
    ACCOUNTS = "accounts"
    REMEMBER = "remember"
    PROXY = "proxy"


class UrlConstants:
    # 外部资源 URL
    MENU_CONFIG_URL = "https://gitee.com/starmcc/qs-beanfun-menu/raw/master/config.json"


class TimeConstants:
    # 时间常量（秒）
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE
    SECONDS_PER_DAY = 24 * SECONDS_PER_HOUR
    SECONDS_PER_WEEK = 7 * SECONDS_PER_DAY

    # 时间常量（毫秒）
    MILLISECONDS_PER_SECOND = 1000
    MILLISECONDS_PER_MINUTE = SECONDS_PER_MINUTE * MILLISECONDS_PER_SECOND
    MILLISECONDS_PER_HOUR = SECONDS_PER_HOUR * MILLISECONDS_PER_SECOND
    MILLISECONDS_PER_DAY = SECONDS_PER_DAY * MILLISECONDS_PER_SECOND


class UiConstants:
    # UI 相关常量
    DEFAULT_BUTTONS_PER_ROW = 4


class BusinessConstants:
    # 业务相关常量
    POINTS_TO_GAME_DIVISOR = Decimal('2.5')
