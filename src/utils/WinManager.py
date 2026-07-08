import locale
import logging

from PySide6.QtCore import QEvent, Qt, QObject, QSize, Slot
from PySide6.QtGui import QIcon, QColor, QPixmap
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QHBoxLayout, QDialog,
                               QGraphicsDropShadowEffect, QPushButton, QMenu, QCheckBox, QRadioButton, QGroupBox,
                               QComboBox, QLineEdit)

from src.config.GlobalConfig import GlobalConstants
from src.config.StyleConstants import StyleConstants
from src.config.TitleBarConfig import TitleBarConfig
from src.utils import MenuManager
from src.zhconv import zhconv


def set_basic_window(window, *, apply_global_style: bool | None = None):
    titleBarConfig: TitleBarConfig = TitleBarConfig()
    from src.window.PyQtBrowser import PyQtBrowser
    from src.window.LoginWeb import LoginWeb
    from src.window.MainWin import MainWin
    from src.window.LoginWin import LoginWin

    if isinstance(window, LoginWin) or isinstance(window, MainWin):
        titleBarConfig.title = f'v {GlobalConstants.APP_VERSION}'
    else:
        titleBarConfig.title = f'{window.windowTitle()} {GlobalConstants.APP_VERSION}'

    if isinstance(window, QDialog):
        if isinstance(window, PyQtBrowser) or isinstance(window, LoginWeb):
            window.setWindowFlags(
                window.windowFlags()
                & ~Qt.WindowType.WindowContextHelpButtonHint
                | Qt.WindowType.WindowMaximizeButtonHint
            )
        else:
            window.setWindowFlags(
                window.windowFlags()
                & ~Qt.WindowType.WindowContextHelpButtonHint
                | Qt.WindowType.MSWindowsFixedSizeDialogHint
            )

    window.setWindowIcon(QIcon(":/images/logo"))

    # apply_global_style=None 时自动判断：
    # - 如果窗口本身已经在 .ui 里设置了 styleSheet，则保留 UI 样式；
    # - 如果窗口没有任何 styleSheet，则套用全局样式。
    if apply_global_style is None:
        apply_global_style = not bool(window.styleSheet().strip())

    if apply_global_style:
        window.setStyleSheet(StyleConstants.GLOBAL_STYLE)
    elif StyleConstants.GLOBAL_STYLE:
        # 把全局样式作为 fallback 注入到没有独立样式的常用子控件。
        __apply_global_style_to_unstyled_children(window)

    if not isinstance(window, QDialog):
        __build_title_bar(window, titleBarConfig)

    __translate_all_controls(window)

    return window

def __apply_global_style_to_unstyled_children(window):

    styled_widget_types = (
        QMenu,
        QLineEdit,
        QPushButton,
    )
    for widget_type in styled_widget_types:
        for widget in window.findChildren(widget_type):
            if not widget.styleSheet().strip():
                widget.setStyleSheet(StyleConstants.GLOBAL_STYLE)


class __WindowDragFilter(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.dragging = False

    def eventFilter(self, obj, event):
        # 鼠标按下：判断是否点击了"非交互控件"（即允许拖动的区域）
        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            # 获取点击的控件
            clicked_widget = self.window.childAt(event.pos())
            # 允许拖动的条件：点击的是窗口本身，或非交互控件（如标签、空白区域）
            if not clicked_widget or isinstance(clicked_widget, (QWidget, QLabel)):
                self.dragging = True
                global_pt = event.globalPosition().toPoint()
                self.start_pos = global_pt - self.window.frameGeometry().topLeft()
                return True  # 拦截事件，用于拖动

        # 鼠标移动：拖动中
        elif event.type() == QEvent.Type.MouseMove and self.dragging:
            move_pt = event.globalPosition().toPoint()
            self.window.move(move_pt - self.start_pos)
            return True

        # 鼠标释放：结束拖动
        elif event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            return True

        # 其他事件不拦截
        return super().eventFilter(obj, event)


def __build_title_bar(window, config: TitleBarConfig):
    TITLE_BAR_HEIGHT = 32
    SHADOW_MARGIN = 6  # 阴影边距，与 PyQt5 版本一致
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    shadow_container = __create_shadow_container()
    background_container = __create_background_container()
    __apply_shadow_effect(shadow_container)
    title_bar = __create_title_bar(window, config, TITLE_BAR_HEIGHT)
    content_widget = __create_content_widget(window)

    __setup_background_layout(background_container, title_bar, content_widget)
    __setup_shadow_layout(shadow_container, background_container, SHADOW_MARGIN)
    __setup_window_layout(window, shadow_container)

    original_size = window.size()
    window.resize(
        original_size.width() + SHADOW_MARGIN * 2,
        original_size.height() + SHADOW_MARGIN * 2 + TITLE_BAR_HEIGHT
    )

    drag_filter = __WindowDragFilter(window)
    window.installEventFilter(drag_filter)


def __create_shadow_container():
    shadow_container = QWidget()
    shadow_container.setObjectName("shadow_container")
    shadow_container.setStyleSheet("""
        #shadow_container {
            background-color: transparent;
            border-radius: 6px;
            overflow: hidden !important;
        }
    """)
    return shadow_container


def __apply_shadow_effect(target_widget):
    """应用阴影效果到目标 widget"""
    shadow = QGraphicsDropShadowEffect(target_widget)
    shadow.setBlurRadius(10)
    shadow.setColor(QColor(0, 0, 0, 80))
    shadow.setOffset(0, 2)
    target_widget.setGraphicsEffect(shadow)


def __create_background_container():
    background_container = QWidget()
    background_container.setObjectName("background_container")
    background_container.setStyleSheet("""
        #background_container {
            background-color: #f5f5f5; 
            border-radius: 10px;
        }
    """)
    return background_container


def __create_title_bar(window, config, height):
    title_bar = QWidget()
    title_bar.setFixedHeight(height)
    title_bar.setStyleSheet("""
        QWidget {
            background-color: #40444F;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
    """)
    title_layout = QHBoxLayout(title_bar)
    title_layout.setContentsMargins(2, 0, 2, 0)
    title_layout.setSpacing(5)

    label_icon = __create_icon(window)
    title_layout.addWidget(label_icon)

    menu_btn = TitleButton(":/images/menu", window)
    title_layout.addWidget(menu_btn)
    title_menu = MenuManager.init_menu(window)
    menu_btn.set_menu(title_menu)

    title_label = QLabel(config.title)
    title_label.setStyleSheet("color: white;")
    title_layout.addWidget(title_label)

    title_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

    if config.min_btn:
        min_btn = TitleButton(":/images/min", window)

        def handle_minimize():
            window.showMinimized()
            window.hide()
            window.trayIcon.showMsg("登录器已最小化到托盘", "QsBeanfun")

        min_btn.clicked.connect(handle_minimize)
        title_layout.addWidget(min_btn)

    if config.max_btn:
        max_btn = TitleButton(":/images/max", window)

        def toggle_maximize():
            if window.isMaximized():
                if hasattr(window, '_original_geometry'):
                    window.setGeometry(window._original_geometry)
                else:
                    window.showNormal()
                max_btn.setText("□")
            else:
                window._original_geometry = window.geometry()
                window.showMaximized()
                max_btn.setText("▢")

        max_btn.clicked.connect(toggle_maximize)
        title_layout.addWidget(max_btn)

    if config.close_btn:
        close_btn = TitleButton(":/images/close", window)
        close_btn.clicked.connect(window.close)
        title_layout.addWidget(close_btn)

    return title_bar


def __create_icon(window):
    icon_label = QLabel(window)
    pixmap = QPixmap(":/images/logo")
    if not pixmap.isNull():
        scaled_pixmap = pixmap.scaled(
            20, 20,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        icon_label.setPixmap(scaled_pixmap)
    icon_label.setStyleSheet("""
        QLabel {
            margin-left: 6px;
            border: none;
            border-radius: 6px;
            background-color: transparent;
        }
    """)
    return icon_label


def __create_content_widget(window):
    content_widget = QWidget()
    content_widget.setObjectName("content_widget")
    content_widget.setStyleSheet("""
        #content_widget {
            background-color: #f5f5f5;
            border-bottom-left-radius: 6px;
            border-bottom-right-radius: 6px;
            padding: 10px;
        }
    """)
    original_layout = window.layout()
    if original_layout:
        content_widget.setLayout(original_layout)
        content_widget.layout().setContentsMargins(0, 0, 0, 0)
    return content_widget


def __setup_background_layout(background_container, title_bar, content_widget):
    bg_layout = QVBoxLayout(background_container)
    bg_layout.setContentsMargins(0, 0, 0, 0)
    bg_layout.setSpacing(0)
    bg_layout.addWidget(title_bar)
    bg_layout.addWidget(content_widget, 1)


def __setup_shadow_layout(shadow_container, background_container, margin=20):
    shadow_layout = QVBoxLayout(shadow_container)
    shadow_layout.setContentsMargins(margin, margin, margin, margin)
    shadow_layout.addWidget(background_container)


def __setup_window_layout(window, shadow_container):
    window.setLayout(QVBoxLayout())
    window.layout().addWidget(shadow_container)
    window.layout().setContentsMargins(0, 0, 0, 0)


def __translate_all_controls(self):
    control_types = (QLabel, QPushButton, QCheckBox, QRadioButton, QGroupBox, QComboBox, QMenu)
    widgets = []
    for cls in control_types:
        widgets.extend(self.findChildren(cls))

    for widget in widgets:
        if hasattr(widget, 'text') and callable(widget.text):
            text = translate(widget.text())
            if hasattr(widget, 'setText') and callable(widget.setText):
                widget.setText(text)
            elif isinstance(widget, QMenu):
                widget.setTitle(text)
    self.setWindowTitle(translate(self.windowTitle()))


def translate(text):
    return zhconv.convert(text, 'zh-cn' if __is_windows_simplified_chinese() else 'zh-tw')


def __is_windows_simplified_chinese():
    try:
        lang, _ = locale.getdefaultlocale()
        simplified_codes = {
            "zh_CN", "zh-CN",
            "zh_Hans_CN",
            "zh_SG", "zh-SG",
            "zh_Hans_SG"
        }
        return lang in simplified_codes
    except Exception as e:
        logging.error(f"获取系统语言时出现异常: {str(e)}")
        return False


class TitleButton(QPushButton):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.init_ui()

    def init_ui(self):
        self.setText("")
        self.setFixedSize(24, 24)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMouseTracking(True)
        self.load_icon()
        self.setStyleSheet("""
            QPushButton {
                color: white;
                border-radius: 6px;
                background-color: transparent;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.11);
            }
        """)

    def load_icon(self):
        pixmap = QPixmap(self.icon_path)
        if pixmap.isNull():
            logging.error(f"警告：无法加载图标 {self.icon_path}")
            self.setText("?")
            return
        scaled_pixmap = pixmap.scaled(
            20, 20,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setIcon(QIcon(scaled_pixmap))
        self.setIconSize(QSize(20, 20))

    def set_menu(self, menu: QMenu):
        self.menu = menu
        self.menu.aboutToHide.connect(self.reset_state)
        self.clicked.connect(self.show_menu)

    def show_menu(self):
        if self.menu:
            self.menu.exec(self.mapToGlobal(self.rect().bottomLeft()))

    @Slot()
    def reset_state(self):
        self.update()
