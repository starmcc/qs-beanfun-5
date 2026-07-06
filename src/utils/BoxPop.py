from typing import Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QInputDialog

from src.utils import WinManager

"""
QMessageBox.Information：用于显示一般的信息消息，通常带有一个信息图标。
QMessageBox.Warning：用于显示警告消息，带有一个警告图标。
QMessageBox.Critical：用于显示严重错误消息，带有一个错误图标。
QMessageBox.Question：用于显示需要用户回答是或否的问题消息，带有一个问号图标。
QMessageBox.NoIcon：不显示任何图标
"""


def err(self, msg) -> bool:
    return show_message_box(self, '错误', msg, QMessageBox.Critical) == QMessageBox.Ok


def warn(self, msg) -> bool:
    return show_message_box(self, '警告', msg, QMessageBox.Warning) == QMessageBox.Ok


def info(self, msg) -> bool:
    return show_message_box(self, '提示', msg, QMessageBox.Information) == QMessageBox.Ok


def question(self, msg) -> bool:
    return show_message_box(self, '请选择', msg, QMessageBox.Question, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes


def custom_question(self, msg, buttons: dict[str, int]) -> int:
    msg_box = QMessageBox(self)
    msg_box.setWindowTitle(WinManager.translate('请选择'))
    msg_box.setText(WinManager.translate(msg))
    msg_box.setIcon(QMessageBox.Information)
    # 添加自定义按钮
    for key, val in buttons.items():
        msg_box.addButton(key, val)
    return msg_box.exec_()


def input_dialog(parent, title: str, label: str) -> Tuple[str, bool]:
    dialog = QInputDialog(parent)
    dialog.setWindowFlags(
        dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    dialog.setInputMode(QInputDialog.TextInput)
    dialog.setWindowTitle(title)
    dialog.setLabelText(label)
    dialog.exec_()
    return dialog.textValue(), dialog.result()


def show_message_box(self, title, text, icon_type=QMessageBox.Information, buttons=QMessageBox.Ok) -> int:
    """
    通用的显示 QMessageBox 的方法。

    :param self: 父窗口对象，如果没有特定父窗口可以设为 None。
    :param title: 消息框标题。
    :param text: 消息框内容文本。
    :param icon_type: 消息框图标类型，可以是 'information'（信息）、'warning'（警告）、'critical'（错误）等。
    :param buttons: 消息框按钮，可以是 QMessageBox.Ok、QMessageBox.Yes | QMessageBox.No 等组合。
    """
    msg_box = QMessageBox(self)
    msg_box.setWindowTitle(WinManager.translate(title))
    msg_box.setText(WinManager.translate(text))
    msg_box.setIcon(icon_type)
    msg_box.setStandardButtons(buttons)
    return msg_box.exec_()
