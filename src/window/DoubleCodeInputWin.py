from PySide6.QtCore import QEvent, Qt, QRegularExpression, QTimer
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QDialog

from src.utils import WinManager
from src.views.UI_DoubleCodeInput import Ui_DoubleCodeInput


class DoubleCodeInputWin(QDialog, Ui_DoubleCodeInput):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        WinManager.set_basic_window(self)
        self.input_code = ""
        self.init_ui()

    def init_ui(self):
        self.pushButton_out.clicked.connect(self.reject)
        self.pushButton_enter.clicked.connect(self.accept)
        self.lineEdit_code.textChanged.connect(self._on_text_change)
        self.lineEdit_code.installEventFilter(self)
        self.lineEdit_code.setFocus()
        validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,6}"))
        self.lineEdit_code.setValidator(validator)
        self.lineEdit_code.setMaxLength(6)

    def eventFilter(self, obj, event):
        if obj is self.lineEdit_code and event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if key in (Qt.Key.Key_Tab, Qt.Key.Key_Backtab):
                return super().eventFilter(obj, event)

            if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if self.input_code:
                    self.pushButton_enter.click()
                return super().eventFilter(obj, event)
        return super().eventFilter(obj, event)

    def _on_text_change(self, text):
        self.input_code = text.strip()
        self.pushButton_enter.setEnabled(bool(self.input_code))
        if len(self.input_code) == 6:
            # 延迟到事件循环空闲时再关闭对话框，避免在 textChanged 信号
            # 处理过程中销毁对话框导致闪退
            QTimer.singleShot(0, self.accept)

    def get_code(self):
        return self.input_code