from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QDialog

from src.utils import WinManager
from src.views.UI_DoubleCodeInput import Ui_DoubleCodeInput


class DoubleCodeInputWin(QDialog, Ui_DoubleCodeInput):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        WinManager.set_basic_window(self)
        self.input_boxes = [
            self.lineEdit_1,
            self.lineEdit_2,
            self.lineEdit_3,
            self.lineEdit_4,
            self.lineEdit_5,
            self.lineEdit_6
        ]
        self.init_ui()
        self.input_code = ""

    def init_ui(self):
        self.pushButton_out.clicked.connect(self.reject)
        self.pushButton_enter.clicked.connect(self.accept)
        for idx, box in enumerate(self.input_boxes):
            box.textChanged.connect(lambda text, idx=idx: self._on_text_change(text, idx))
            box.installEventFilter(self)
        self.lineEdit_1.setFocus()

    def eventFilter(self, obj, event):
        if obj in self.input_boxes and event.type() == QEvent.KeyPress:
            key = event.key()
            idx = self.input_boxes.index(obj)

            # 处理删除键
            if key == Qt.Key_Backspace and idx > 0:
                if idx == len(self.input_boxes) - 1 and self.input_boxes[idx].text():
                    self.input_boxes[idx].clear()
                    return True

                self.input_boxes[idx - 1].setFocus()
                self.input_boxes[idx - 1].clear()
                return True

            # 允许Tab键
            if key == Qt.Key_Tab:
                return super().eventFilter(obj, event)  # 不拦截Tab键，交给系统处理

            # 3.按键的文本内容判断是否为数字
            pressed_char = event.text()
            if not pressed_char.isdigit():
                # 非数字字符 → 拦截，不允许输入
                return True
        return super().eventFilter(obj, event)

    def _on_text_change(self, text, idx):
        if text and len(text) == 1:
            if idx < 5:
                self.input_boxes[idx + 1].setFocus()
        self.input_code = "".join([box.text() for box in self.input_boxes])
        self.pushButton_enter.setEnabled(len(self.input_code) == 6)

    def get_code(self):
        return self.input_code
