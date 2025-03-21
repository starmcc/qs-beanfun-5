from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QInputDialog

"""
QMessageBox.Information：用于显示一般的信息消息，通常带有一个信息图标。
QMessageBox.Warning：用于显示警告消息，带有一个警告图标。
QMessageBox.Critical：用于显示严重错误消息，带有一个错误图标。
QMessageBox.Question：用于显示需要用户回答是或否的问题消息，带有一个问号图标。
QMessageBox.NoIcon：不显示任何图标
"""


def err(self, msg) -> bool:
    return __show_message_box(self, 'Error', msg, QMessageBox.Information) == QMessageBox.Ok


def warn(self, msg) -> bool:
    return __show_message_box(self, 'Warning', msg, QMessageBox.Warning) == QMessageBox.Ok


def info(self, msg) -> bool:
    return __show_message_box(self, 'tips', msg, QMessageBox.Information) == QMessageBox.Ok


def question(self, msg) -> bool:
    return __show_message_box(self, 'select', msg, QMessageBox.Question, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes


def input_dialog(parent, title: str, label: str) -> (str, bool):
    dialog = QInputDialog(parent)
    dialog.setWindowFlags(
        dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    dialog.setInputMode(QInputDialog.TextInput)
    dialog.setWindowTitle(title)
    dialog.setLabelText(label)
    dialog.exec_()
    return dialog.textValue(), dialog.result()


def __show_message_box(self, title, text, icon_type=QMessageBox.Information, buttons=QMessageBox.Ok) -> int:
    """
    通用的显示 QMessageBox 的方法。

    :param self: 父窗口对象，如果没有特定父窗口可以设为 None。
    :param title: 消息框标题。
    :param text: 消息框内容文本。
    :param icon_type: 消息框图标类型，可以是 'information'（信息）、'warning'（警告）、'critical'（错误）等。
    :param buttons: 消息框按钮，可以是 QMessageBox.Ok、QMessageBox.Yes | QMessageBox.No 等组合。
    """
    msg_box = QMessageBox(self)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setIcon(icon_type)
    msg_box.setStandardButtons(buttons)
    return msg_box.exec_()

# def __show_message_box(self, title, text, icon_type=QMessageBox.Information, buttons=QMessageBox.Ok):
#     """
#     通用的显示 QMessageBox 的方法。
#
#     :param self: 父窗口对象，如果没有特定父窗口可以设为 None。
#     :param title: 消息框标题。
#     :param text: 消息框内容文本。
#     :param icon_type: 消息框图标类型，可以是 'information'（信息）、'warning'（警告）、'critical'（错误）等。
#     :param buttons: 消息框按钮，可以是 QMessageBox.Ok、QMessageBox.Yes | QMessageBox.No 等组合。
#     """
#
#     def task(param):
#         a1, a2, a3, a4, a5 = param
#         msg_box = QMessageBox(a1)
#         msg_box.setWindowTitle(a2)
#         msg_box.setText(a3)
#         msg_box.setIcon(a4)
#         msg_box.setStandardButtons(a5)
#         msg_box.exec_()
#
#     from src.config.GlobalConfig import GLOBAL_CONFIG
#     GLOBAL_CONFIG.custom_queue.addTask(task, (self, title, text, icon_type, buttons))
