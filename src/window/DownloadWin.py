import time

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QDialog, QVBoxLayout, QWidget

from src.utils import WinManager
from src.views.Ui_Download import Ui_Download


class DownloadWin(QDialog, Ui_Download):
    """独立的下载进度窗口，提供美观的下载反馈界面"""

    # 进度更新信号（线程安全）
    progress_signal = Signal(int)
    # 状态文字更新信号
    status_signal = Signal(str)
    # 速度更新信号
    speed_signal = Signal(str)
    # 用户关闭窗口请求取消信号
    cancel_requested = Signal()

    def __init__(self, parent=None, title: str = "下载", status: str = "正在连接服务器..."):
        super().__init__(parent)
        self.setupUi(self)
        # 模态窗口：更新下载期间禁止操作主窗口
        self.setModal(True)
        WinManager.set_basic_window(self)
        self._init_ui()
        self._connect_signals()
        # 设置窗口标题和初始状态（titleLabel 保留 .ui 中的默认文字）
        self.setWindowTitle(title)
        self.statusLabel.setText(status)

    def _init_ui(self):
        # 将下载动画放入 animFrame 中
        self.anim_widget = _DownloadAnimation()
        anim_layout = QVBoxLayout(self.animFrame)
        anim_layout.setContentsMargins(0, 0, 0, 0)
        anim_layout.addWidget(self.anim_widget)

    def set_title(self, text: str):
        """设置窗口标题和标题文字"""
        self.setWindowTitle(text)
        self.titleLabel.setText(text)

    def _connect_signals(self):
        self.progress_signal.connect(self._on_progress)
        self.status_signal.connect(self._on_status)
        self.speed_signal.connect(self._on_speed)

    def _on_progress(self, value: int):
        self.progressBar.setValue(value)
        self.percentLabel.setText(f"{value}%")

    def _on_status(self, text: str):
        self.statusLabel.setText(text)

    def _on_speed(self, text: str):
        self.speedLabel.setText(text)

    def set_progress(self, value: int):
        """线程安全地更新进度"""
        self.progress_signal.emit(value)

    def set_status(self, text: str):
        """线程安全地更新状态文字"""
        self.status_signal.emit(text)

    def set_speed(self, text: str):
        """线程安全地更新下载速度"""
        self.speed_signal.emit(text)

    def closeEvent(self, event):
        if hasattr(self, 'anim_widget'):
            self.anim_widget.stop()
        # 通知外部取消后台下载任务
        self.cancel_requested.emit()
        super().closeEvent(event)


class _DownloadAnimation(QWidget):
    """下载动画 - 旋转的圆环"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(72, 72)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_angle)
        self.timer.start(30)

    def _update_angle(self):
        self.angle = (self.angle + 10) % 360
        self.update()

    def stop(self):
        if self.timer.isActive():
            self.timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 背景圆环
        pen = QPen(QColor(230, 234, 240), 6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(6, 6, 60, 60, 0, 360 * 16)

        # 前景旋转圆环
        pen = QPen(QColor(66, 135, 245), 6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(6, 6, 60, 60, self.angle * 16, 270 * 16)

        painter.end()
