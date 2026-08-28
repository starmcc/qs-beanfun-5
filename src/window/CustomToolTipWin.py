from PySide6.QtCore import Qt, QPoint, QRect, QObject
from PySide6.QtGui import QFont, QCursor
from PySide6.QtWidgets import QLabel

from src.config.StyleConstants import StyleConstants
from src.utils import WinManager
from src.config.I18n import I18N


class __CustomToolTipWin(QObject):
    def __init__(self, parent, target_widget, text):
        super().__init__(parent)
        self.parent = parent
        self.target_widget = target_widget
        self.tip_text = text
        self.tooltip = None

        self.tooltip = self._create_tooltip()
        self.tooltip.setText(WinManager.translate(text))
        I18N.language_changed.connect(lambda _language: self._refresh_text())
        font = QFont("Microsoft YaHei", 13)
        self.tooltip.setFont(font)
        self.tooltip.adjustSize()

        # 给目标控件 + 父窗口同时挂载事件过滤器，监听所有状态
        self.target_widget.installEventFilter(self)
        self.parent.installEventFilter(self)

        # 控件销毁自动清理提示框
        self.target_widget.destroyed.connect(self._cleanup)

    def _create_tooltip(self):
        tooltip = QLabel(self.parent)
        tooltip.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.FramelessWindowHint
        )
        tooltip.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        tooltip.hide()
        tooltip.setStyleSheet(StyleConstants.TIPS_WIN_STYLE)
        return tooltip

    def _refresh_text(self):
        if self.tooltip:
            self.tooltip.setText(WinManager.translate(self.tip_text))
            self.tooltip.adjustSize()

    def _hide_tip(self):
        if self.tooltip and self.tooltip.isVisible():
            self.tooltip.hide()

    def _cleanup(self):
        self._hide_tip()
        if self.tooltip:
            self.tooltip.deleteLater()
            self.tooltip = None

    def eventFilter(self, watched, event):
        # 父窗口隐藏/最小化/关闭时隐藏提示
        if watched == self.parent:
            if event.type() == event.Type.Hide or event.type() == event.Type.Close:
                self._hide_tip()
            return super().eventFilter(watched, event)

        # 目标控件鼠标事件
        if watched == self.target_widget:
            if event.type() == event.Type.Enter:
                self._on_mouse_enter()
            elif event.type() == event.Type.Leave:
                self._on_mouse_leave()
            elif event.type() == event.Type.MouseMove:
                if self.tooltip and self.tooltip.isVisible():
                    self._update_position()
            # 窗口失去焦点隐藏提示
            elif event.type() == event.Type.FocusOut:
                self._hide_tip()
        # 返回False，不拦截原生事件，hover样式正常生效
        return False

    def _on_mouse_enter(self):
        self._update_position()
        self.tooltip.show()

    def _on_mouse_leave(self):
        self._hide_tip()

    def _update_position(self):
        if not self.target_widget or not self.tooltip:
            return

        mouse_pos = QCursor.pos()
        tooltip_width = self.tooltip.width()
        tooltip_height = self.tooltip.height()
        screen_geometry = self.parent.screen().geometry()

        tooltip_x = mouse_pos.x() + 10
        tooltip_y = mouse_pos.y() + 10

        widget_rect = QRect(
            self.target_widget.mapToGlobal(QPoint(0, 0)),
            self.target_widget.size()
        )
        tooltip_rect = QRect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)

        if widget_rect.intersects(tooltip_rect):
            if widget_rect.right() + 10 + tooltip_width <= screen_geometry.right():
                tooltip_x = widget_rect.right() + 10
                tooltip_y = widget_rect.top() + (widget_rect.height() - tooltip_height) // 2
            elif widget_rect.left() - 10 - tooltip_width >= screen_geometry.left():
                tooltip_x = widget_rect.left() - 10 - tooltip_width
                tooltip_y = widget_rect.top() + (widget_rect.height() - tooltip_height) // 2
            elif widget_rect.bottom() + 10 + tooltip_height <= screen_geometry.bottom():
                tooltip_x = widget_rect.left() + (widget_rect.width() - tooltip_width) // 2
                tooltip_y = widget_rect.bottom() + 10
            elif widget_rect.top() - 10 - tooltip_height >= screen_geometry.top():
                tooltip_x = widget_rect.left() + (widget_rect.width() - tooltip_width) // 2
                tooltip_y = widget_rect.top() - 10 - tooltip_height

        if tooltip_x + tooltip_width > screen_geometry.right():
            tooltip_x = mouse_pos.x() - tooltip_width - 10
        if tooltip_y + tooltip_height > screen_geometry.bottom():
            tooltip_y = mouse_pos.y() - tooltip_height - 10

        self.tooltip.move(tooltip_x, tooltip_y)


def build_tips(parent, target_widget, text) -> __CustomToolTipWin:
    return __CustomToolTipWin(parent, target_widget, text)