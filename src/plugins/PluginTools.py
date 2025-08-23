import os
import zipfile

from PyQt5.QtCore import QFile, QIODevice

from src.plugins.Plugins import Plugins
from src.utils import BaseTools


def build_plugin(pg: Plugins) -> str:
    # 目录构建
    plugin_directory = BaseTools.build_path(rf'plugins\{os.path.splitext(pg.plugin_name)[0]}')
    # 检查目录是否存在
    if not os.path.exists(plugin_directory):
        # 创建目录
        os.makedirs(plugin_directory, exist_ok=True)
    # 检查文件是否存在,存在则返回不作处理
    for file in pg.files:
        file_path = os.path.join(plugin_directory, file)
        if os.path.isfile(file_path):
            return plugin_directory

    # 从qrc资源中读取ZIP文件内容
    qrc_file_path = f":/plugins/{pg.plugin_name}"
    qfile = QFile(qrc_file_path)

    if not qfile.open(QIODevice.ReadOnly):
        raise FileNotFoundError(f"无法从qrc中读取插件: {qrc_file_path}")

    # 将ZIP文件内容写入临时文件
    temp_zip_path = os.path.join(plugin_directory, f"temp_{pg.plugin_name}")
    with open(temp_zip_path, 'wb') as f:
        f.write(qfile.readAll().data())
    qfile.close()

    # 解压逻辑
    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        zip_ref.extractall(plugin_directory)

    # 删除临时文件
    os.remove(temp_zip_path)
    return plugin_directory
