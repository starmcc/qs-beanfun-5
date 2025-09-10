import locale
import logging

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEvent, Qt, QObject
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel, QHBoxLayout, QDialog, QGraphicsDropShadowEffect

from src.config.GlobalConfig import GLOBAL_APP_VERSION
from src.config.TitleBarConfig import TitleBarConfig
from src.utils import MenuManager
from src.zhconv import zhconv


def set_basic_window(window):
    titleBarConfig: TitleBarConfig = TitleBarConfig()
    from src.window.PyQtBrowser import PyQtBrowser
    from src.window.LoginWin import LoginWin
    if isinstance(window, LoginWin):
        titleBarConfig.title = f'v {GLOBAL_APP_VERSION}'
    else:
        titleBarConfig.title = f'{window.windowTitle()} {GLOBAL_APP_VERSION}'

    if isinstance(window, QDialog):
        if isinstance(window, PyQtBrowser):
            window.setWindowFlags(window.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.WindowMaximizeButtonHint)
        else:
            window.setWindowFlags(window.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    # 设置全局样式
    __build_default_global_style(window)
    # 创建窗口为无边框，构建标题栏
    if not isinstance(window, QDialog):
        __build_title_bar(window, titleBarConfig)
    # 转换组件文字语言
    __translate_all_controls(window)

    return window


class __WindowDragFilter(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.dragging = False

    def eventFilter(self, obj, event):
        # 鼠标按下：判断是否点击了"非交互控件"（即允许拖动的区域）
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            # 获取点击的控件
            clicked_widget = self.window.childAt(event.pos())
            # 允许拖动的条件：点击的是窗口本身，或非交互控件（如标签、空白区域）
            if not clicked_widget or isinstance(clicked_widget, (QWidget, QLabel)):
                self.dragging = True
                self.start_pos = event.globalPos() - self.window.frameGeometry().topLeft()
                return True  # 拦截事件，用于拖动

        # 鼠标移动：拖动中
        elif event.type() == QEvent.MouseMove and self.dragging:
            self.window.move(event.globalPos() - self.start_pos)
            return True

        # 鼠标释放：结束拖动
        elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            self.dragging = False
            return True

        # 其他事件不拦截
        return super().eventFilter(obj, event)


def __build_default_global_style(window):
    window.setWindowIcon(QIcon(":/images/logo"))

    window.setStyleSheet("""
        * {
        font-family: 'Microsoft YaHei', 'SimHei', 'Arial', sans-serif;
        }

        QLineEdit {
        border: 1px solid #a0a0a0;  /* 边框宽度为 1px，颜色为 #a0a0a0 */
        border-radius: 3px;  /* 边框圆角 */
        padding-left: 5px;  /* 文本距离左边界有 5px */
        background-color: transparent;  /* 背景颜色 */
        color: black;  /* 文本颜色 */
        selection-background-color: #F57C00;  /* 选中文本的背景颜色 */
        font-size: 10pt;  /* 文本字体大小 */
        }

        QLineEdit:hover {  /* 鼠标悬浮在 QLineEdit 时的状态 */
            border: 1px solid #F57C00;
            border-radius: 3px;
            background-color: #f2f2f2;
            color: #F57C00;
            selection-background-color: #F57C00;
        }

        QLineEdit[echoMode="2"] {  /* QLineEdit 有输入掩码时的状态 */
            lineedit-password-character: 9679;
        }
        """)


def __build_title_bar(window, config: TitleBarConfig):
    TITLE_BAR_HEIGHT = 32

    # 设置无边框和透明背景
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setAttribute(Qt.WA_TranslucentBackground)

    # 创建各部分组件
    shadow_container = __create_shadow_container()
    background_container = __create_background_container()
    title_bar = __create_title_bar(window, config, TITLE_BAR_HEIGHT)
    content_widget = __create_content_widget(window)

    # 组装所有容器层级
    __setup_background_layout(background_container, title_bar, content_widget)
    __setup_shadow_layout(shadow_container, background_container)
    __setup_window_layout(window, shadow_container)

    # 调整窗口大小
    original_size = window.size()
    window.resize(
        original_size.width() + 12,
        original_size.height() + 12 + TITLE_BAR_HEIGHT
    )

    # 事件过滤器（允许拖动标题栏）
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

    # 添加阴影效果
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setColor(QColor(0, 0, 0, 80))
    shadow.setOffset(0, 2)
    shadow_container.setGraphicsEffect(shadow)

    return shadow_container


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

    # 标题栏布局
    title_layout = QHBoxLayout(title_bar)
    title_layout.setContentsMargins(2, 0, 2, 0)
    title_layout.setSpacing(5)

    # 添加菜单按钮
    menu_btn = __create_menu_button(window)
    title_layout.addWidget(menu_btn)
    title_menu = MenuManager.init_menu(window)
    # 动态获取菜单
    MenuManager.build_dynamic_menu(window, title_menu)

    # 按钮点击事件：显示菜单
    def show_menu_by_button():
        # # 菜单显示在按钮的左下角（相对于按钮）
        button_pos = menu_btn.mapToGlobal(QtCore.QPoint(0, menu_btn.height()))
        title_menu.exec_(button_pos)

    menu_btn.clicked.connect(show_menu_by_button)

    # 添加标题文本
    title_label = QLabel(config.title)
    title_label.setStyleSheet("color: white;")
    title_layout.addWidget(title_label)

    # 占位符（推挤按钮到右侧）
    title_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    # 添加控制按钮
    if config.min_btn:
        min_btn = __create_minimize_button(window)
        title_layout.addWidget(min_btn)

    if config.max_btn:
        max_btn = __create_maximize_button(window)
        title_layout.addWidget(max_btn)

    if config.close_btn:
        close_btn = __create_close_button(window)
        title_layout.addWidget(close_btn)

    return title_bar


def __create_menu_button(window):
    menu_btn = QPushButton()
    menu_btn.setIcon(QIcon(":/images/logo"))
    menu_btn.setFixedSize(24, 24)
    menu_btn.setFocusPolicy(Qt.NoFocus)
    menu_btn.setStyleSheet("""
        QPushButton {
            border: 0; 
            border-radius: 6px; 
            background-color: transparent; 
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.2); 
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.3); 
        }
    """)
    return menu_btn


def __create_minimize_button(window):
    min_btn = QPushButton("—")
    min_btn.setFixedSize(28, 28)
    min_btn.setFocusPolicy(Qt.NoFocus)
    min_btn.setStyleSheet("""
        QPushButton {
            color: white;
            border: 0; 
            border-radius: 6px; 
            background-color: transparent; 
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.2); 
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.3); 
        }
    """)

    def handle_minimize():
        window.showMinimized()
        window.hide()  # 隐藏窗口
        window.trayIcon.showMsg("登录器已最小化到托盘")

    min_btn.clicked.connect(handle_minimize)
    return min_btn


def __create_maximize_button(window):
    max_btn = QPushButton("□")
    max_btn.setFixedSize(28, 28)
    max_btn.setFocusPolicy(Qt.NoFocus)
    max_btn.setStyleSheet("""
        QPushButton {
            color: white;
            border: 0; 
            border-radius: 6px; 
            background-color: transparent; 
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.2); 
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.3); 
        }
    """)

    window._original_geometry = None

    def toggle_maximize():
        if window.isMaximized():
            if window._original_geometry:
                window.setGeometry(window._original_geometry)
            else:
                window.showNormal()
            max_btn.setText("□")
        else:
            window._original_geometry = window.geometry()
            window.showMaximized()
            max_btn.setText("▢")

    max_btn.clicked.connect(toggle_maximize)
    return max_btn


def __create_close_button(window):
    close_btn = QPushButton("X")
    close_btn.setFixedSize(28, 28)
    close_btn.setFocusPolicy(Qt.NoFocus)
    close_btn.setStyleSheet("""
        QPushButton {
            color: white;
            border: 0; 
            border-radius: 6px; 
            background-color: transparent; 
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.2); 
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.3); 
        }
    """)
    close_btn.clicked.connect(window.close)
    return close_btn


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

    # 迁移原窗口内容
    original_layout = window.layout()
    if original_layout:
        content_widget.setLayout(original_layout)
        content_widget.layout().setContentsMargins(0, 0, 0, 0)

    return content_widget


def __setup_background_layout(background_container, title_bar, content_widget):
    # 背景容器的布局（标题栏 + 内容区）
    bg_layout = QVBoxLayout(background_container)
    bg_layout.setContentsMargins(0, 0, 0, 0)
    bg_layout.setSpacing(0)
    bg_layout.addWidget(title_bar)
    bg_layout.addWidget(content_widget, 1)


def __setup_shadow_layout(shadow_container, background_container):
    # 阴影容器的布局（只包含背景容器）
    shadow_layout = QVBoxLayout(shadow_container)
    shadow_layout.setContentsMargins(6, 6, 6, 6)  # 阴影边距
    shadow_layout.addWidget(background_container)


def __setup_window_layout(window, shadow_container):
    # 窗口最终布局
    window.setLayout(QVBoxLayout())
    window.layout().addWidget(shadow_container)
    window.layout().setContentsMargins(0, 0, 0, 0)


def __translate_all_controls(self):
    # 定义需要转换文本的控件类型
    control_types = (QtWidgets.QLabel, QtWidgets.QPushButton, QtWidgets.QCheckBox,
                     QtWidgets.QRadioButton, QtWidgets.QGroupBox, QtWidgets.QComboBox,
                     QtWidgets.QAction, QtWidgets.QMenu)
    # 查找所有指定类型的控件
    widgets = self.findChildren(control_types)
    for widget in widgets:
        if hasattr(widget, 'text') and callable(widget.text):
            # 进行简转繁
            text = translate(widget.text())
            if hasattr(widget, 'setText') and callable(widget.setText):
                widget.setText(text)
            elif isinstance(widget, QtWidgets.QMenu):
                widget.setTitle(text)
    # 转换窗口标题
    self.setWindowTitle(translate(self.windowTitle()))


def translate(text):
    return zhconv.convert(text, 'zh-cn' if __is_windows_simplified_chinese() else 'zh-tw')


def __is_windows_simplified_chinese():
    try:
        # 获取系统默认语言环境
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
