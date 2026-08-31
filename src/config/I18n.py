# -*- coding: utf-8 -*-
# 轻量级国际化支持。
from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from src.config import GlobalConfig

# 仅维护应用自身 UI 文本，不依赖在线服务或大型离线翻译库。
ENGLISH_DICT: dict[str, str] = {
    "语言": "Language",
    "简体中文": "Simplified Chinese",
    "繁體中文": "Traditional Chinese",
    "设置": "Settings",
    "常规设置": "General",
    "阻止游戏更新": "No updates",
    "跳过 Play 窗口": "Skip Play",
    "跳过登录界面": "Skip login",
    "工具自动检查更新": "Auto update",
    "使用GGM获取密令": "Get OTP Codes via GGM",
    "游戏目录": "Game directory",
    "请选择新枫之谷游戏安装目录": "Select the MapleStory installation directory",
    "尚未选择游戏目录": "No game directory selected",
    "浏览目录": "Browse",
    "启动游戏": "Start game",
    "用户中心": "User center",
    "会员中心": "Membership center",
    "储值中心": "Recharge center",
    "客服中心": "Customer service",
    "账号详情": "Account details",
    "登出": "Log out",
    "实用功能": "Tools",
    "强制结束NGS进程": "Force close NGS process",
    "强制结束游戏": "Force close game",
    "系统计算器": "Calculator",
    "下载GGM插件": "Download GGM",
    "安装枫之谷经典版": "Install MapleStory Classic",
    "获取新版本": "Check for updates",
    "关于..": "About",
    "退出": "Exit",
    "是否立即结束Ngs进程?": "Close the NGS process now?",
    "是否强制结束游戏?": "Force close the game?",
    "下载失败，状态码:": "Download failed, status code:",
    "下载GGM插件失败": "Failed to download GGM",
    "启动GGM安装程序失败": "Failed to start the GGM installer",
    "未找到Nexon Game Manager安装路径，请先下载安装Nexon Game Manager插件": "Nexon Game Manager was not found. Download and install it first.",
    "启动Nexon Game Manager安装经典版失败": "Failed to start the MapleStory Classic installer",
    "忘记密码": "Forgot password",
    "注册账号": "Register",
    "台湾": "TW",
    "香港": "HK",
    "账号": "Act",
    "记住密码": "Remember",
    "密码": "Pwd",
    "账号管理": "Manager",
    "登录": "Log in",
    "官网登入": "Official website",
    "自动填入": "Auto Input",
    "数字账号": "ID",
    "正常": "Normal",
    "封禁": "Banned",
    "乐豆": "Points",
    "动态密令": "Code",
    "游戏账号": "Game ID",
    "账号状态": "Status",
    "最大账号创建数量：-": "Max accounts: -",
    "最大账号创建数量：": "Max accounts: ",
    "新建账号": "Add",
    "经典版": "Classic",
    "获取密令": "Get code",
    "登录验证": "Login verification",
    "台服进阶验证": "Taiwan advanced verification",
    "请填写图形验证码与手机号码后继续登录": "Enter the captcha and phone number to continue",
    "点击图片刷新": "Click image to refresh",
    "图形验证码": "Captcha",
    "请输入图形验证码": "Enter captcha",
    "提示资料": "Information",
    "手机号码": "Phone number",
    "请输入手机号码": "Enter phone number",
    "确认送出": "Submit",
    "二维码登入": "QR code login",
    "便捷导航": "Quick navigation",
    "游戏常用导航": "Game shortcuts",
    "支持搜索筛选，点击按钮可快速打开站点或二维码": "Search and filter shortcuts, then open a site or QR code",
    "输入关键字搜索功能入口...": "Search shortcuts...",
    "默认浏览器": "Default browser",
    "刷新": "Refresh",
    "双重验证": "Two-factor authentication",
    "请输入验证码": "Enter verification code",
    "请输入授权验证器中的数字验证码": "Enter the numeric code from your authenticator",
    "取消": "Cancel",
    "确定": "OK",
    "账号管理 - 双击可选择对应账号应用": "Accounts",
    "本地账号管理": "Accounts",
    "双击行可快速应用账号，右键可新增、编辑、删除或刷新": "Double-click to use. Right-click to add/edit/delete/refresh.",
    "账号地区": "Region",
    "最后登录时间": "Last login",
    "增加": "Add",
    "编辑": "Edit",
    "删除": "Del",
    "是否删除账号[{account}]?": "Delete account [{account}]?",
    "关于": "About",
    "关于本程序与使用说明": "About this application and usage",
    "重要提示": "Important notice",
    "如果您条件允许，望君赞赏": "If you can, please consider supporting us",
    "您的支持是持续维护与优化的动力": "Your support keeps the project maintained and improved",
    "作者 QQ": "Author QQ",
    "本程式不是游戏橘子数位科技开发的客户端程序": "This program is not a client developed by Gamania Digital Entertainment",
    "使用本程式请确保下载途径是否为作者提供的下载途径": "Please ensure you download this program from the author's official channel",
    "使用本程式造成的一切后果由使用者承担": "The user assumes all consequences arising from the use of this program",
    "所有不怀好意的指责...都需要时间去验证！": "All malicious accusations... need time to be verified!",
    "天": "days",
    "您的账号已建立了": "Your account has been established for",
    "编辑名称": "Edit name",
    "编辑账号": "Edit account",
    "请填写账号信息并选择登录地区": "Enter account information and select a region",
    "备注": "Note",
    "请输入账号": "Enter account",
    "请输入密码": "Enter password",
    "可选，用于区分账号": "Optional, for identifying the account",
    "保存": "Save",
    "等待": "Please wait...",
    "请稍后...": "Please wait...",
    "显示": "Show",
    "QsBeanfun\n双击：显示/隐藏窗口\n右键：打开菜单": "QsBeanfun\nDouble-click: show/hide window\nRight-click: open menu",
    "程序已最小化到托盘": "Minimized to tray",
    "正在安全退出...": "Exiting safely...",
    "前往发布页": "Open release page",
    "立即更新": "Update now",
    "不再提醒": "Don't remind",
    "无法获取版本信息": "Unable to get version info",
    "当前是最新版本": "Already up to date",
    "错误": "Error",
    "警告": "Warning",
    "提示": "Info",
    "请选择": "Select",
    "暂无数据": "No data",
    "禁止": "Disabled",
    "未知错误": "Unknown error",
    "网络错误": "Network error",
    "请输入验证码!": "Enter code!",
    "请输入手机号码!": "Enter phone number!",
    "请输入账号昵称": "Enter account nickname",
    "修改账号名称": "Edit account name",
    "请输入新的账号名称": "Enter new account name",
    "操作异常！": "Operation failed!",
    "获取动态密令失败": "Failed to get code",
    "自动输入失败,请手动复制输入!": "Auto input failed. Copy and enter manually!",
    "获取登录数据失败": "Failed to get login data",
    "获取账号信息失败!": "Failed to get account info!",
    "未知错误,无法获得Beanfun信息!": "Unknown error. Failed to get Beanfun info!",
    "此账号尚未完成进阶认证,请前往会员中心完成后【重新登录】!": "Advanced verification is incomplete. Finish it in Member Center, then log in again!",
    "此账号尚未完成电话进阶认证\n请前往会员中心完成后重新登录！": "Phone verification is incomplete.\nFinish it in Member Center, then log in again!",
    "谷歌人机验证/邮箱验证/门号验证/疑难杂症等..\n点击打开内置浏览器进行原生态登入操作": "For reCAPTCHA, email, phone verification, etc.\nOpen the built-in browser for official login.",
    "使用【GamaPass】进行台湾账号登录\n适用于已绑定【GamaPass】的账号\n游玩【经典版】必须使用【GamaPass】登入": "Use GamaPass for TW account login.\nFor accounts already linked to GamaPass.\nClassic requires GamaPass login.",
    "启动游戏将直接跳过登录界面\n与网页登录相似\n不建议开启该功能": "Skip the login screen when launching the game.\nSimilar to web login.\nNot recommended.",
    "由于连接台服可能存在网络波动导致更新失败\n一般情况下请默认勾选阻止游戏自动更新\n建议通过官网下载最新补丁手动更新": "TW server connection may cause update failures.\nUsually keep game auto-update blocked.\nDownload patches manually from the official site.",
    "每次启动工具检查版本更新\n取消勾选则不检查": "Check for tool updates on startup.\nUncheck to skip checks.",
    "《新枫之谷》启动后,会打开默认启动页\n建议勾选自动关闭该启动页\n该启动页无任何作用,加快游戏启动速度": "MapleStory opens a default start page after launch.\nAuto-close it to speed up startup.",
    "使用 GGM（Gamania Games Manager）获取动态密令\n需要本地已安装 GGM 才能生效": "Get OTP codes via GGM.\nRequires local GGM installation.\nPrompt to install GGM if missing",
    "选择游戏目录\n请选择英文目录": "Select the game folder.\nUse an English-only path.",
    "账户拥有的储值点数": "Stored points for this account",
    "如显示封禁请立刻联系官方客服解除!\n菜单 -> 用户中心 -> 客服中心 -> 联系客服 -> 填写信息并等待客服邮件回复\n建议勿使用外挂/辅助/宏/VPN等软件\n官方一经查实永久封禁,误封可解除": "If banned, contact official support immediately.\nMenu -> User Center -> Customer Service -> Contact Support.\nAvoid cheats, helpers, macros, VPNs, etc.\nConfirmed violations may cause permanent bans; false bans can be appealed.",
    "勾选后点击获取密令将自动聚焦《新枫之谷》\n并自动在游戏中输入数字账号和动态密令": "When checked, Get code will focus MapleStory\nand enter the ID and code automatically.",
    "勾选后只会从系统默认浏览器打开网址": "Open links only in the default browser when checked",
}


class I18n(QObject):
    """全局语言状态和变更通知。"""

    language_changed = Signal(str)
    _instance: "I18n | None" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        super().__init__()
        # 直接读取已保存的语言配置；若读取失败则回退简体中文。
        self._language = GlobalConfig.LANGUAGE.ZH_CN.value
        try:
            from src.config import Config
            saved = Config.language()
            if saved in (GlobalConfig.LANGUAGE.ZH_CN.value, GlobalConfig.LANGUAGE.ZH_TW.value, GlobalConfig.LANGUAGE.EN.value):
                self._language = saved
        except Exception:
            pass
        self._initialized = True

    @property
    def language(self) -> str:
        return self._language

    def set_language(self, language: str) -> None:
        if language not in (GlobalConfig.LANGUAGE.ZH_CN.value, GlobalConfig.LANGUAGE.ZH_TW.value, GlobalConfig.LANGUAGE.EN.value):
            language = GlobalConfig.LANGUAGE.ZH_CN.value
        if self._language == language:
            return
        self._language = language
        try:
            from src.config import Config
            Config.language(language)
        except Exception:
            pass
        self.language_changed.emit(language)

    def translate(self, text: str) -> str:
        if self._language == GlobalConfig.LANGUAGE.EN.value:
            if text in ENGLISH_DICT:
                return ENGLISH_DICT[text]
            # 动态数量文本保留数字，只翻译固定前缀。
            if text.startswith("最大账号创建数量："):
                return "Max accounts: " + text.split("：", 1)[1]
            if text.startswith("发现新版本：") and text.endswith("\n是否立即更新?"):
                content = text[len("发现新版本："):]
                return "New version found: " + content.rsplit("\n是否立即更新?", 1)[0] + "\nUpdate now?"
            if text.startswith("于 ") and text.endswith(" 创建"):
                return "Created at " + text[2:-3]
            if text.startswith("等待App确认登录\n请在") and text.endswith("秒内进行操作!"):
                seconds = text.split("请在", 1)[1].split("秒内", 1)[0]
                return f"Waiting for app login confirmation\nOperate within {seconds}s!"
            if text.startswith("启动游戏出现了问题:\n "):
                return "Failed to start game:\n " + text.split("\n ", 1)[1]
            if text.startswith("启动经典版游戏出现了问题:\n "):
                return "Failed to start Classic:\n " + text.split("\n ", 1)[1]
            if text.startswith("下载GGM插件失败:\n"):
                return "Failed to download GGM:\n" + text.split("\n", 1)[1]
            if text.startswith("启动GGM安装程序失败:\n"):
                return "Failed to start the GGM installer:\n" + text.split("\n", 1)[1]
            if text.startswith("启动Nexon Game Manager安装经典版失败:\n"):
                return "Failed to start MapleStory Classic installer:\n" + text.split("\n", 1)[1]
        return text


class _I18NProxy:
    """惰性单例代理：首次访问时才实例化 I18n。

    避免在模块加载阶段（Config 尚未加载完成）触发循环导入。
    """

    def __getattr__(self, name):
        return getattr(I18n(), name)


I18N = _I18NProxy()


def tr(text: str) -> str:
    return I18N.translate(text)
