from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QPalette
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout,
                             QGraphicsDropShadowEffect, QGraphicsBlurEffect)


class LoadingMask(QWidget):

    def __init__(self, parent=None, text="Loading...", blur_radius=10):
        super().__init__(parent)
        # 1. 基础配置（覆盖父控件、模糊透明背景）
        self.setParent(parent)
        self.setFixedSize(parent.size())

        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 半透明背景
        # 创建主容器，用于承载模糊效果和内容
        self.container = QWidget(self)
        self.setContentsMargins(6, 6, 6, 6)

        # 设置模糊效果
        self.blur_effect = QGraphicsBlurEffect(self)
        self.blur_effect.setBlurRadius(blur_radius)  # 模糊半径，值越大越模糊
        self.container.setGraphicsEffect(self.blur_effect)

        # 设置半透明背景色
        palette = self.container.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255, 180))  # 最后一个参数是透明度(0-255)
        self.container.setPalette(palette)
        self.container.setAutoFillBackground(True)

        # 2. 加载动画 + 文字布局（居中显示）
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignCenter)

        # 加载动画（使用自定义绘制的动画，不依赖GIF）
        self.anim_widget = LoadingAnimation()
        # 确保动画不受背景模糊影响
        self.anim_widget.setGraphicsEffect(None)

        # 加载文字（简洁字体）
        self.text_label = QLabel(text)
        self.text_label.setFont(QFont("Microsoft YaHei", 12, QFont.Medium))
        self.text_label.setStyleSheet("color: #333333;")
        # 确保文字不受背景模糊影响
        self.text_label.setGraphicsEffect(None)

        # 3. 添加阴影效果（提升精致感）
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 3)
        self.container.setGraphicsEffect(shadow)

        # 4. 组装布局
        self.layout.addWidget(self.anim_widget)
        self.layout.addSpacing(15)
        self.layout.addWidget(self.text_label)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)

    def closeEvent(self, a0):
        self.hide()
        self.deleteLater()
        super().closeEvent(a0)


class LoadingAnimation(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(64, 64)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_angle)
        self.timer.start(30)  # 控制动画速度

    def update_angle(self):
        self.angle = (self.angle + 10) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        # 绘制背景圆环
        pen = QPen(QColor(220, 220, 220), 6)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawArc(QRectF(6, 6, 52, 52), 0, 360 * 16)

        # 绘制旋转的前景圆环
        pen = QPen(QColor(66, 135, 245), 6)  # 蓝色，可根据需要调整
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        # 绘制3/4圆的弧，随角度旋转
        painter.drawArc(QRectF(6, 6, 52, 52), self.angle * 16, 270 * 16)

    def closeEvent(self, event):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        super().closeEvent(event)