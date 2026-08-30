import locale
import logging

from PySide6.QtCore import QEvent, Qt, QObject
from PySide6.QtGui import QIcon, QColor, QPixmap
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QHBoxLayout, QDialog,
                               QGraphicsDropShadowEffect, QPushButton, QMenu, QCheckBox, QRadioButton, QGroupBox,
                               QComboBox, QLineEdit, QMessageBox)

from src.components.TitleButton import TitleButton
from src.config import GlobalConfig
from src.config.GlobalConfig import GlobalConstants
from src.config.I18n import I18N, tr
from src.config.TitleBarConfig import TitleBarConfig
from src.utils import MenuManager
from src.zhconv import zhconv


def set_basic_window(window):
    if getattr(window, '_custom_title_bar_initialized', False):
        if not getattr(window, '_i18n_connected', False):
            I18N.language_changed.connect(lambda _language: __translate_all_controls(window))
            window._i18n_connected = True
        __translate_all_controls(window)
        return window

    titleBarConfig = __create_title_bar_config(window)
    __apply_native_window_flags(window)
    window.setWindowIcon(QIcon(":/images/logo"))

    if not __is_browser_window(window):
        __build_title_bar(window, titleBarConfig)
        window._custom_title_bar_initialized = True

    if not getattr(window, '_i18n_connected', False):
        def refresh_window(_language):
            __translate_all_controls(window)
            title_label = getattr(window, '_title_bar_label', None)
            if title_label is not None:
                source = title_label.property('_i18n_source_text') or title_label.text()
                title_label.setText(translate(source))

        I18N.language_changed.connect(refresh_window)
        window._i18n_connected = True
    __translate_all_controls(window)
    return window


def __create_title_bar_config(window) -> TitleBarConfig:
    from src.window.MainWin import MainWin
    from src.window.LoginWin import LoginWin

    is_primary_window = isinstance(window, (LoginWin, MainWin))
    title = f'v {GlobalConstants.APP_VERSION}' if is_primary_window else window.windowTitle()
    return TitleBarConfig(
        title=title,
        min_btn=is_primary_window,
        max_btn=False,
        close_btn=True
    )


def __is_browser_window(window) -> bool:
    from src.components.PyQtBrowser import PyQtBrowser
    from src.components.LoginWeb import LoginWeb
    from src.components.RecaptchaWeb import RecaptchaWindow

    return isinstance(window, (PyQtBrowser, LoginWeb, RecaptchaWindow))


def __apply_native_window_flags(window):
    base_flags = window.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint

    if isinstance(window, QMessageBox):
        window.setWindowFlags(base_flags)
        return

    if __is_browser_window(window):
        window.setWindowFlags(base_flags)
        return

    if isinstance(window, QDialog):
        window.setWindowFlags(base_flags | Qt.WindowType.MSWindowsFixedSizeDialogHint)


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
    TITLE_BAR_HEIGHT = 36
    SHADOW_MARGIN = 6
    new_flags = (window.windowFlags()
                 & ~Qt.WindowType.WindowTitleHint
                 & ~Qt.WindowType.WindowSystemMenuHint
                 & ~Qt.WindowType.WindowMinMaxButtonsHint
                 & ~Qt.WindowType.WindowCloseButtonHint)
    new_flags |= Qt.WindowType.FramelessWindowHint
    window.setWindowFlags(new_flags)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    shadow_container = __create_shadow_container()
    background_container = __create_background_container()
    __apply_shadow_effect(shadow_container)
    title_bar = __create_title_bar(window, config, TITLE_BAR_HEIGHT)
    content_widget = __create_content_widget(window)

    __setup_background_layout(background_container, title_bar, content_widget)
    __setup_shadow_layout(shadow_container, background_container, SHADOW_MARGIN)
    __setup_window_layout(window, shadow_container)

    __resize_window_for_custom_title_bar(window, TITLE_BAR_HEIGHT, SHADOW_MARGIN)

    drag_filter = __WindowDragFilter(window)
    window._title_bar_drag_filter = drag_filter
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
    title_layout.setContentsMargins(6, 0, 6, 0)
    title_layout.setSpacing(4)
    title_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

    label_icon = __create_icon(window)
    title_layout.addWidget(label_icon)

    if config.min_btn:
        menu_btn = TitleButton(":/images/menu", window)
        title_layout.addWidget(menu_btn)
        title_menu = MenuManager.init_menu(window)
        menu_btn.set_menu(title_menu)
        window._title_menu_button = menu_btn
        window._title_menu = title_menu

        def refresh_menu(_language):
            old_menu = getattr(window, '_title_menu', None)
            new_menu = MenuManager.init_menu(window)
            menu_btn.set_menu(new_menu)
            window._title_menu = new_menu
            if old_menu is not None:
                old_menu.deleteLater()

        window._i18n_menu_refresh = refresh_menu
        I18N.language_changed.connect(refresh_menu)

    title_label = QLabel(translate(config.title))
    title_label.setProperty('_i18n_source_text', config.title)
    title_label.setFixedHeight(height)
    window._title_bar_label = title_label
    title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    title_label.setStyleSheet("color: white; padding-bottom: 1px;")
    title_layout.addWidget(title_label, 0, Qt.AlignmentFlag.AlignVCenter)

    title_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

    if config.min_btn:
        min_btn = TitleButton(":/images/min", window)

        def handle_minimize():
            window.showMinimized()
            if hasattr(window, 'trayIcon'):
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
    icon_label.setFixedSize(20, 20)
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap(":/images/logo")
    if not pixmap.isNull():
        scaled_pixmap = pixmap.scaled(
            18, 18,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        icon_label.setPixmap(scaled_pixmap)
    icon_label.setStyleSheet("""
        QLabel {
            margin-left: 2px;
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


def __resize_window_for_custom_title_bar(window, title_bar_height, shadow_margin):
    if window.testAttribute(Qt.WidgetAttribute.WA_Resized):
        original_size = window.size()
    else:
        size_hint = window.sizeHint()
        original_size = size_hint if size_hint.isValid() else window.size()

    window.resize(
        original_size.width() + shadow_margin * 2,
        original_size.height() + shadow_margin * 2 + title_bar_height
    )


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
    control_types = (QLabel, QPushButton, QCheckBox, QRadioButton, QGroupBox, QComboBox, QLineEdit, QMenu)
    widgets = []
    for cls in control_types:
        widgets.extend(self.findChildren(cls))

    for widget in widgets:
        if isinstance(widget, QMenu):
            source = widget.property('_i18n_source_title')
            if source is None:
                source = widget.title()
                widget.setProperty('_i18n_source_title', source)
            widget.setTitle(translate(source))
            continue
        if hasattr(widget, 'text') and callable(widget.text):
            source = widget.property('_i18n_source_text')
            if source is None:
                source = widget.text()
                widget.setProperty('_i18n_source_text', source)
            if hasattr(widget, 'setText') and callable(widget.setText):
                widget.setText(translate(source))
        if isinstance(widget, QLineEdit):
            placeholder = widget.property('_i18n_source_placeholder')
            if placeholder is None:
                placeholder = widget.placeholderText()
                widget.setProperty('_i18n_source_placeholder', placeholder)
            if placeholder:
                widget.setPlaceholderText(translate(placeholder))
    source_title = self.property('_i18n_source_window_title')
    if source_title is None:
        source_title = self.windowTitle()
        self.setProperty('_i18n_source_window_title', source_title)
    self.setWindowTitle(translate(source_title))


def translate(text):
    translated = tr(text)
    if I18N.language == GlobalConfig.LANGUAGE.EN.value:
        return translated
    if I18N.language == GlobalConfig.LANGUAGE.ZH_TW.value:
        return zhconv.convert(translated, 'zh-tw')
    return zhconv.convert(translated, 'zh-cn')


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
