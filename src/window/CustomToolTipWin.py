from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import QLabel

from src.config.StyleConstants import StyleConstants
from src.utils import WinManager


class __CustomToolTipWin:

    def __init__(self, parent, target_widget, text):
        self.parent = parent
        self.tooltip = self._create_tooltip()
        self.tooltip.setText(WinManager.translate(text))
        font = QFont("Microsoft YaHei", 13)
        self.tooltip.setFont(font)
        self.tooltip.adjustSize()
        self.target_widget = target_widget

        # 绑定鼠标事件
        self.target_widget.enterEvent = self._on_mouse_enter
        self.target_widget.leaveEvent = self._on_mouse_leave
        self.target_widget.mouseMoveEvent = self._on_mouse_move  # 监听鼠标移动

    def _create_tooltip(self):
        """创建提示框控件"""
        tooltip = QLabel(self.parent)
        tooltip.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.FramelessWindowHint
        )
        tooltip.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        tooltip.hide()  # 初始隐藏

        tooltip.setStyleSheet(StyleConstants.TIPS_WIN_STYLE)
        return tooltip

    def _on_mouse_enter(self, event):
        """鼠标进入控件时显示提示框"""
        self._update_position()
        self.tooltip.show()
        event.accept()

    def _on_mouse_leave(self, event):
        """鼠标离开控件时隐藏提示框"""
        self.tooltip.hide()
        event.accept()

    def _on_mouse_move(self, event):
        """鼠标在控件内移动时更新提示框位置"""
        if self.tooltip.isVisible():
            self._update_position()
        event.accept()

    def _update_position(self):
        if not self.target_widget:
            return

        # 1. 获取基础位置数据
        mouse_pos = QCursor.pos()  # 鼠标全局位置
        tooltip_width = self.tooltip.width()
        tooltip_height = self.tooltip.height()
        screen_geometry = self.parent.screen().geometry()  # 屏幕区域

        # 2. 计算初始位置（鼠标右下方偏移10px）
        tooltip_x = mouse_pos.x() + 10
        tooltip_y = mouse_pos.y() + 10

        # 3. 检查是否遮挡目标控件，若遮挡则调整
        # 获取目标控件的全局矩形区域
        widget_rect = QRect(
            self.target_widget.mapToGlobal(QPoint(0, 0)),
            self.target_widget.size()
        )
        # 提示框当前位置的矩形区域
        tooltip_rect = QRect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)

        # 若提示框与控件重叠，则调整位置到控件外部
        if widget_rect.intersects(tooltip_rect):
            # 优先尝试显示在控件右侧
            if widget_rect.right() + 10 + tooltip_width <= screen_geometry.right():
                tooltip_x = widget_rect.right() + 10
                tooltip_y = widget_rect.top() + (widget_rect.height() - tooltip_height) // 2
            # 其次尝试显示在控件左侧
            elif widget_rect.left() - 10 - tooltip_width >= screen_geometry.left():
                tooltip_x = widget_rect.left() - 10 - tooltip_width
                tooltip_y = widget_rect.top() + (widget_rect.height() - tooltip_height) // 2
            # 再尝试显示在控件下方
            elif widget_rect.bottom() + 10 + tooltip_height <= screen_geometry.bottom():
                tooltip_x = widget_rect.left() + (widget_rect.width() - tooltip_width) // 2
                tooltip_y = widget_rect.bottom() + 10
            # 最后尝试显示在控件上方
            elif widget_rect.top() - 10 - tooltip_height >= screen_geometry.top():
                tooltip_x = widget_rect.left() + (widget_rect.width() - tooltip_width) // 2
                tooltip_y = widget_rect.top() - 10 - tooltip_height

        # 4. 屏幕边界检查（超出屏幕时调整）
        if tooltip_x + tooltip_width > screen_geometry.right():
            tooltip_x = mouse_pos.x() - tooltip_width - 10
        if tooltip_y + tooltip_height > screen_geometry.bottom():
            tooltip_y = mouse_pos.y() - tooltip_height - 10

        # 5. 应用最终位置
        self.tooltip.move(tooltip_x, tooltip_y)


def build_tips(parent, target_widget, text) -> __CustomToolTipWin:
    return __CustomToolTipWin(parent, target_widget, text)