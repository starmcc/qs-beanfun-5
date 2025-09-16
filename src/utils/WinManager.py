import locale
import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent, Qt, QObject, QSize, pyqtSlot
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QHBoxLayout, QDialog, QGraphicsDropShadowEffect, QPushButton, QMenu

from src.config.GlobalConfig import GLOBAL_APP_VERSION
from src.config.StyleConstants import StyleConstants
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
    window.setWindowIcon(QIcon(":/images/logo"))
    window.setStyleSheet(StyleConstants.GLOBAL_STYLE)
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

    # 添加图标
    label_icon = __create_icon(window)
    title_layout.addWidget(label_icon)

    # 添加菜单按钮
    menu_btn = TitleButton(":/images/menu", window)
    title_layout.addWidget(menu_btn)
    title_menu = MenuManager.init_menu(window)
    # 动态获取菜单
    MenuManager.build_dynamic_menu(window, title_menu)
    # 关联按钮菜单
    menu_btn.set_menu(title_menu)

    # 添加标题文本
    title_label = QLabel(config.title)
    title_label.setStyleSheet("color: white;")
    title_layout.addWidget(title_label)

    # 占位符（推挤按钮到右侧）
    title_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    # 添加控制按钮
    if config.min_btn:
        min_btn = TitleButton(":/images/min", window)

        def handle_minimize():
            window.showMinimized()
            window.hide()  # 隐藏窗口
            window.trayIcon.showMsg("登录器已最小化到托盘")

        min_btn.clicked.connect(handle_minimize)
        title_layout.addWidget(min_btn)

    if config.max_btn:
        max_btn = TitleButton(":/images/max", window)

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
        title_layout.addWidget(max_btn)

    if config.close_btn:
        close_btn = TitleButton(":/images/close", window)
        close_btn.clicked.connect(window.close)
        title_layout.addWidget(close_btn)

    return title_bar


def __create_icon(window):
    icon_label = QLabel(window)
    # 加载图标（支持资源文件路径或本地文件路径）
    pixmap = QPixmap(":/images/logo")  # 使用QPixmap加载图标
    if not pixmap.isNull():
        scaled_pixmap = pixmap.scaled(
            20, 20,
            Qt.KeepAspectRatio,  # 保持宽高比
            Qt.SmoothTransformation  # 平滑缩放
        )
        icon_label.setPixmap(scaled_pixmap)

    # 设置样式（无边框、透明背景）
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


class TitleButton(QPushButton):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path  # 图标路径
        self.init_ui()

    def init_ui(self):
        # 基础设置
        self.setText("")  # 不显示文字
        self.setFixedSize(24, 24)  # 固定尺寸
        self.setFocusPolicy(Qt.NoFocus)  # 去除焦点框
        self.setAttribute(Qt.WA_StyledBackground, True)  # 确保样式生效
        self.setMouseTracking(True)  # 启用鼠标跟踪

        # 加载并设置图标
        self.load_icon()

        # 设置交互样式（简洁可靠）
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
        """加载图标并处理可能的错误"""
        pixmap = QPixmap(self.icon_path)
        if pixmap.isNull():
            # 图标加载失败
            logging.error(f"警告：无法加载图标 {self.icon_path}")
            self.setText("?")
            return

        # 缩放图标以适应按钮（保持比例）
        scaled_pixmap = pixmap.scaled(
            20, 20,  # 稍小于按钮尺寸，留边距
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation  # 平滑缩放
        )
        self.setIcon(QIcon(scaled_pixmap))
        self.setIconSize(QSize(20, 20))  # 图标显示尺寸

    def set_menu(self, menu: QMenu):
        """设置关联的菜单并监听关闭事件"""
        self.menu = menu
        # 菜单即将隐藏时重置按钮状态
        self.menu.aboutToHide.connect(self.reset_state)
        # 将按钮点击与菜单弹出关联
        self.clicked.connect(self.show_menu)

    def show_menu(self):
        """显示菜单（在按钮下方）"""
        if self.menu:
            # 菜单显示位置：按钮下方左侧对齐
            self.menu.exec_(self.mapToGlobal(self.rect().bottomLeft()))

    @pyqtSlot()
    def reset_state(self):
        """重置按钮状态，清除按压效果"""
        self.update()
