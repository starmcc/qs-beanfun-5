# 加载 UI 文件
from enum import Enum

from src.utils.TaskQueue import TaskQueue
from typing import Any, Iterable, Optional


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

    # 限制可用属性以减少内存与误赋值
    __slots__ = (
        "_bf_web_token",
        "_now_login_type",
        "win_main",
        "win_actManager",
        "win_config",
        "win_accountInfo",
        "win_about",
        "win_nav",
        "win_twAdv",
        "win_intermediateLogin",
        "win_qrCode",
        "custom_queue",
        "_initialized",
    )

    def __new__(cls, *args, **kwargs):
        """实现单例模式，确保全局只有一个实例"""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # 防止重复初始化（单例模式必要处理）
        if hasattr(self, "_initialized"):
            return

        # 令牌与登录类型
        self.bf_web_token = ""
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

        self.now_login_type = ""

        self._initialized = True  # 标记初始化完成

    # ================= 属性与工具方法 =================
    @property
    def bf_web_token(self) -> str:
        return self._bf_web_token

    @bf_web_token.setter
    def bf_web_token(self, value: Optional[str]) -> None:
        self._bf_web_token = value or ""

    @property
    def now_login_type(self) -> str:
        return self._now_login_type

    @now_login_type.setter
    def now_login_type(self, value: Optional[str]) -> None:
        # 兼容传入 ActType 或 str
        if value is None:
            self._now_login_type = ""
            return
        if isinstance(value, ActType):
            self._now_login_type = value.value
            return
        self._now_login_type = str(value)

    def clear_token(self) -> None:
        """清空登录令牌。"""
        self._bf_web_token = ""

    def _safe_close(self, obj: Any) -> None:
        try:
            if obj is None:
                return
            # QDialog/QWidget 兼容关闭
            if hasattr(obj, "close"):
                obj.close()
            if hasattr(obj, "deleteLater"):
                obj.deleteLater()
        except Exception:
            pass

    def close_window(self, attr_name: str) -> bool:
        """关闭并清理指定窗口属性。返回是否成功处理。"""
        if not hasattr(self, attr_name):
            return False
        obj = getattr(self, attr_name)
        self._safe_close(obj)
        try:
            setattr(self, attr_name, None)
        except Exception:
            # 在 __slots__ 下依然安全，除非 attr_name 非法
            return False
        return True

    def close_windows(self, names: Iterable[str]) -> None:
        for name in names:
            self.close_window(name)

    def close_all_dialogs(self) -> None:
        """关闭所有可能存在的对话框/子窗口。"""
        self.close_windows((
            "win_actManager",
            "win_config",
            "win_accountInfo",
            "win_about",
            "win_nav",
            "win_twAdv",
            "win_intermediateLogin",
            "win_qrCode",
        ))

    def reset_login(self) -> None:
        """重置登录态并关闭临时验证窗口。"""
        self.clear_token()
        self.close_windows(("win_twAdv", "win_intermediateLogin", "win_qrCode"))


# 全局配置实例（单例）
GLOBAL_CONFIG = _GlobalConfig()
