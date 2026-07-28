from typing import Tuple, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QInputDialog, QDialog, QAbstractButton

from src.utils import WinManager

"""
QMessageBox.Icon.Information：用于显示一般的信息消息，通常带有一个信息图标。
QMessageBox.Icon.Warning：用于显示警告消息，带有一个警告图标。
QMessageBox.Icon.Critical：用于显示严重错误消息，带有一个错误图标。
QMessageBox.Icon.Question：用于显示需要用户回答是或否的问题消息，带有一个问号图标。
QMessageBox.Icon.NoIcon：不显示任何图标
"""


def err(self, msg) -> bool:
    return show_message_box(self, '错误', msg, QMessageBox.Icon.Critical) == QMessageBox.StandardButton.Ok


def warn(self, msg) -> bool:
    return show_message_box(self, '警告', msg, QMessageBox.Icon.Warning) == QMessageBox.StandardButton.Ok


def info(self, msg) -> bool:
    return show_message_box(self, '提示', msg, QMessageBox.Icon.Information) == QMessageBox.StandardButton.Ok


def question(self, msg) -> bool:
    btn_flag = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    return show_message_box(self, '请选择', msg, QMessageBox.Icon.Question, btn_flag) == QMessageBox.StandardButton.Yes


def custom_question(self, msg, buttons: dict[str, QMessageBox.ButtonRole]) -> QMessageBox.ButtonRole:
    msg_box = QMessageBox(self)
    msg_box.setWindowTitle(WinManager.translate('请选择'))
    msg_box.setText(WinManager.translate(msg))
    msg_box.setIcon(QMessageBox.Icon.Information)
    # 清除全部默认标准按钮
    msg_box.setStandardButtons(QMessageBox.StandardButton.NoButton)

    # 批量添加自定义按钮
    for text, role in buttons.items():
        msg_box.addButton(text, role)

    # 弹出弹窗，等待点击
    msg_box.exec()
    # 返回点击的按钮对象
    return msg_box.buttonRole(msg_box.clickedButton())


def input_dialog(parent, title: str, label: str) -> Tuple[str, bool]:
    dialog = QInputDialog(parent)
    dialog.setWindowFlags(
        dialog.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint | Qt.WindowType.MSWindowsFixedSizeDialogHint)
    dialog.setInputMode(QInputDialog.InputMode.TextInput)
    dialog.setWindowTitle(title)
    dialog.setLabelText(label)
    dialog.exec()
    return dialog.textValue(), dialog.result() == QDialog.DialogCode.Accepted


def show_message_box(self, title, text, icon_type=QMessageBox.Icon.Information, buttons=QMessageBox.StandardButton.Ok) -> int:
    """
    通用的显示 QMessageBox 的方法。

    :param self: 父窗口对象，如果没有特定父窗口可以设为 None。
    :param title: 消息框标题。
    :param text: 消息框内容文本。
    :param icon_type: 消息框图标类型，可以是 Information、Warning、Critical 等。
    :param buttons: 消息框按钮，可以是 StandardButton.Ok、Yes | No 等组合。
    """
    msg_box = QMessageBox(self)
    msg_box.setWindowTitle(WinManager.translate(title))
    msg_box.setText(WinManager.translate(text))
    msg_box.setIcon(icon_type)
    msg_box.setStandardButtons(buttons)
    return msg_box.exec()