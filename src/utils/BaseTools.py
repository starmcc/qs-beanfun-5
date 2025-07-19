import importlib
import logging
import os
import shutil
import sys
import webbrowser
import zipfile

from PyQt5.QtCore import QFile, QIODevice
from packaging import version

from src.client import RequestClient
from src.config import GlobalConfig
from src.config.GlobalConfig import GLOBAL_APP_GITHUB_API, GLOBAL_APP_GITHUB
from src.utils import BoxPop


def hidden_str(s):
    if s and len(s) > 5:
        return s[:5] + '*' * (len(s) - 5)
    else:
        return s


def build_path(path: str, env: bool = False):
    if not env and getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        p = os.path.dirname(sys.executable)
        return rf'{p}\{path}'
    # 如果是在开发环境中运行
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    p = os.path.dirname(p)
    return rf'{p}\{path}'


def extract_build_plugin(plugin_name):
    # 创建目标目录
    plugin_directory = build_path(rf'plugins\{os.path.splitext(plugin_name)[0]}')
    os.makedirs(plugin_directory, exist_ok=True)

    # 从qrc资源中读取ZIP文件内容
    qrc_file_path = f":/plugins/{plugin_name}"
    qfile = QFile(qrc_file_path)

    if not qfile.open(QIODevice.ReadOnly):
        raise FileNotFoundError(f"无法从qrc中读取插件: {qrc_file_path}")

    # 将ZIP文件内容写入临时文件
    temp_zip_path = os.path.join(plugin_directory, f"temp_{plugin_name}")
    with open(temp_zip_path, 'wb') as f:
        f.write(qfile.readAll().data())
    qfile.close()

    # 解压逻辑
    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        zip_ref.extractall(plugin_directory)

    # 删除临时文件
    os.remove(temp_zip_path)

    return plugin_directory


def check_version(self):
    try:
        response = RequestClient.get_instance().get(f"{GLOBAL_APP_GITHUB_API}/releases/latest")
        response.raise_for_status()
        data = response.json()
        latest_version = data.get('tag_name')
        if latest_version is None:
            BoxPop.err(self, "无法获取版本信息")
            return
        try:
            if version.parse(GlobalConfig.GLOBAL_APP_VERSION) >= version.parse(latest_version):
                BoxPop.info(self, "当前已是最新版本")
            elif BoxPop.question(self, f"发现新版本 {latest_version}，是否前往更新？"):
                webbrowser.open(f'{GLOBAL_APP_GITHUB}/releases')
        except version.InvalidVersion as e:
            logging.error(f"解析版本失败{e}")
            BoxPop.err(self, "解析版本失败")
    except ValueError as e:
        logging.error(f"解析 JSON 出错: {e}")
        BoxPop.err(self, "解析版本失败2")


def build_chrome():
    # 构建QtWebEngineProcess的复制品chrome.exe 适配加速器
    spec = importlib.util.find_spec('PyQt5')
    if spec and spec.submodule_search_locations:
        pyqt5_dir = spec.submodule_search_locations[0]
        possible_path = os.path.join(pyqt5_dir, 'Qt5', 'bin', 'QtWebEngineProcess.exe')
        if os.path.exists(possible_path):
            # 构建目标文件路径
            target_path = os.path.join(os.path.dirname(possible_path), 'chrome.exe')
            # 复制文件
            if not os.path.exists(target_path):
                shutil.copy2(possible_path, target_path)
                logging.info(f"已初始化 {target_path}")
            return target_path
    return None
