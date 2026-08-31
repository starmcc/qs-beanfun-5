import importlib
import logging
import os
import shutil
import sys


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
    """检查新版本（兼容入口，委托给 UpdaterClient）"""
    # 延迟导入，避免与 RequestClient -> Config -> BaseTools 形成循环导入
    from src.client.updater.UpdaterClient import UpdaterClient
    UpdaterClient.check_new_version(win, quiet)


def build_chrome():
    """将 QtWebEngineProcess.exe 复制为 chrome.exe，使游戏加速器识别为浏览器进程并放行流量。
    兼容开发环境（PySide6 site-packages）和 PyInstaller 打包后（_internal 目录）两种场景。"""
    # 优先查找 PySide6 中的 QtWebEngineProcess.exe
    spec = importlib.util.find_spec('PySide6')
    if spec and spec.submodule_search_locations:
        pyside6_dir = spec.submodule_search_locations[0]
        source_path = os.path.join(pyside6_dir, 'QtWebEngineProcess.exe')
    else:
        # PyInstaller 打包后：QtWebEngineProcess.exe 在 _internal 目录
        base_dir = os.path.dirname(sys.executable)
        source_path = os.path.join(base_dir, '_internal', 'QtWebEngineProcess.exe')

    if not os.path.exists(source_path):
        logging.warning(f"未找到 QtWebEngineProcess.exe: {source_path}")
        return None

    target_path = os.path.join(os.path.dirname(source_path), 'chrome.exe')
    if os.path.exists(target_path):
        logging.info(f"chrome.exe 已存在: {target_path}")
        return target_path

    try:
        shutil.copy2(source_path, target_path)
        logging.info(f"已创建 chrome.exe: {target_path}")
        return target_path
    except Exception as e:
        logging.error(f"创建 chrome.exe 失败: {e}")
        return None


def check_cn_path(path):
    if not path:
        return False
    for char in path:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False
