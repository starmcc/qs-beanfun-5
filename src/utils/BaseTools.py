import importlib
import logging
import os
import shutil
import sys
import webbrowser
from datetime import datetime

from PyQt5.QtWidgets import QMessageBox
from packaging import version

from src.client import RequestClient
from src.config import Config
from src.config.GlobalConfig import GlobalConstants
from src.utils import BoxPop
from src.utils.ThreadPoolManager import get_thread_pool


def hidden_str(s):
    if s and len(s) > 5:
        return s[:5] + '*' * (len(s) - 5)
    else:
        return s


def build_path(path: str):
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        p = os.path.dirname(sys.executable)
        return rf'{p}\{path}'
    # 如果是在开发环境中运行
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    return rf'{p}\{path}'


def check_new_version(win, quiet: bool = True):
    # 检查更新
    def __check_update_result(window, result, e):
        # 安静模式且24小时内提醒过则返回
        if quiet and (dt := Config.update_tips_time()):
            if (datetime.now() - dt).total_seconds() <= 604800:
                return
        if not result:
            result = (False, '未知错误')
        status_flag, message = result
        if e:
            logging.error(f"检查版本更新出现错误：\n {str(e)}")
            status_flag = False
            message = "无法获取版本信息"
        if status_flag:
            buttons = {
                "前往更新": QMessageBox.AcceptRole,
                "取消": QMessageBox.RejectRole
            }
            if quiet:
                buttons = {
                    "前往更新": QMessageBox.AcceptRole,
                    "本周不提醒": QMessageBox.ActionRole,
                    "取消": QMessageBox.RejectRole
                }
            click_result = BoxPop.custom_question(window, message, buttons)

            if click_result == 0:
                webbrowser.open(f"{GlobalConstants.GITHUB_URL}/releases")
            if quiet and click_result == 1:
                Config.update_tips_time(datetime.now())

        elif not quiet:
            BoxPop.info(window, message)

    get_thread_pool().submit_task(__check_version, __check_update_result, win, not quiet)


def __check_version() -> (bool, str):
    # bool = 是否有更新
    # str = 更新内容,错误消息
    msg = '无法获取版本信息'
    response = RequestClient.get_instance().get(f"{GlobalConstants.GITHUB_API_URL}/releases/latest")
    response.raise_for_status()
    data = response.json()
    latest_version = data.get('tag_name')
    if latest_version is None:
        return False, msg
    if version.parse(GlobalConstants.APP_VERSION) >= version.parse(latest_version) and getattr(sys, 'frozen', False):
        return False, '当前是最新版本'
    else:
        body = data.get('body')
        msg = f'发现新版本：{latest_version}\n{body}\n是否前往更新?'
        return True, msg


def build_chrome():
    # 构建QtWebEngineProcess的复制品chrome.exe 适配加速器
    spec = importlib.util.find_spec('PyQt5')
    if spec and spec.submodule_search_locations:
        pyqt5_dir = spec.submodule_search_locations[0]
        # 构建目标文件路径
        possible_path = os.path.join(pyqt5_dir, 'Qt5', 'bin', 'QtWebEngineProcess.exe')
        target_path = os.path.join(os.path.dirname(possible_path), 'chrome.exe')
        if os.path.exists(possible_path) and not os.path.exists(target_path):
            # 复制文件
            shutil.copy2(possible_path, target_path)
            os.chmod(target_path, 0o777)
            logging.info(f"已初始化 {target_path}")
        return target_path
    return None


def check_cn_path(path):
    if not path:
        return False
    for char in path:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False
