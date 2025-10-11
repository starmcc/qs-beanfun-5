import logging
import os
from pathlib import Path

from PyQt5.QtCore import QFile, QIODevice

from src.plugins.Plugins import Plugins
from src.utils import BaseTools

VERSION_FILE_NAME = 'version.qs'


def build_plugin(plugin: Plugins) -> str:
    """构建插件目录和文件"""
    plugin_directory = BaseTools.build_path(rf'plugins\{plugin.plugin_name}')
    os.makedirs(plugin_directory, exist_ok=True)

    version_file_path = os.path.join(plugin_directory, VERSION_FILE_NAME)
    version_matches = _is_version_match(version_file_path, plugin.version)
    files_complete = version_matches and _check_files_exist(plugin_directory, plugin.files)

    if version_matches and files_complete:
        return plugin_directory

    # 确定需要写入的文件
    if version_matches and not files_complete:
        files_to_write = _get_missing_files(plugin_directory, plugin.files)
    else:
        files_to_write = plugin.files

    # 写入文件
    success_count = 0
    for file_name in files_to_write:
        if _write_qrc_file(plugin_directory, plugin.plugin_name, file_name):
            success_count += 1

    # 更新版本文件
    try:
        with open(version_file_path, 'w', encoding='utf-8') as f:
            f.write(plugin.version)
    except Exception as e:
        logging.error(f"写入插件版本文件失败: {e}")

    logging.info(f"插件 {plugin.plugin_name} 构建完成: {success_count}/{len(files_to_write)} 个文件成功")
    return plugin_directory


def _is_version_match(version_file_path: str, expected_version: str) -> bool:
    """检查版本是否匹配"""
    if not os.path.exists(version_file_path):
        return False

    try:
        with open(version_file_path, 'r', encoding='utf-8') as f:
            return f.read().strip() == expected_version
    except Exception as e:
        logging.error(f"读取插件版本文件失败: {e}")
        return False


def _check_files_exist(plugin_directory: str, expected_files) -> bool:
    """检查所有文件是否存在"""
    return all((Path(plugin_directory) / f).exists() for f in expected_files)


def _get_missing_files(plugin_directory: str, expected_files) -> list:
    """获取缺失的文件列表"""
    return [f for f in expected_files if not (Path(plugin_directory) / f).exists()]


def _write_qrc_file(plugin_directory: str, plugin_name: str, file_name: str) -> bool:
    """从qrc资源中读取文件并写入到插件目录"""
    qrc_file_path = f":/plugins/{plugin_name}/{file_name}"
    target_file_path = Path(plugin_directory) / file_name

    try:
        target_file_path.parent.mkdir(parents=True, exist_ok=True)

        qfile = QFile(qrc_file_path)
        if not qfile.exists() or not qfile.open(QIODevice.ReadOnly):
            logging.error(f"无法读取qrc文件: {qrc_file_path}")
            return False

        file_data = qfile.readAll()
        qfile.close()

        with open(target_file_path, 'wb') as f:
            f.write(file_data.data() if hasattr(file_data, 'data') else bytes(file_data))

        return True
    except Exception as e:
        logging.error(f"写入插件文件失败 {file_name}: {e}")
        return False