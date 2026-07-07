import logging
import typing
import webbrowser
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QGroupBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from src.client import RequestClient
from src.config.GlobalConfig import GlobalConstants
from src.utils import WinManager
from src.utils.ThreadPoolManager import get_thread_pool
from src.views.UI_Nav import Ui_Nav
from src.window import PyQtBrowser, CustomToolTipWin
from src.window.QrCodeShowWin import QrCodeShowWin


class NavWin(QDialog, Ui_Nav):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        WinManager.set_basic_window(self)
        self._raw_entries: List[dict] = []
        self._flat_items: List[Dict[str, Any]] = []
        self._build_ui()
        self._load_entries()

    def _build_ui(self):
        self.pushButton_refresh.clicked.connect(self._load_entries)
        self.lineEdit_search.textChanged.connect(self._filter_entries)
        CustomToolTipWin.build_tips(self, self.checkBox_outer, "勾选后只会从系统默认浏览器打开网址")

    def _load_entries(self):
        def _result(win, entry, e):
            win._raw_entries = entry or []
            if e:
                logging.error(f"发生错误:\n{str(e)}")
                return
            win._render_groups(win._raw_entries)

        get_thread_pool().submit_task(self._get_dynamic_nav_config, _result, self, True)

    def _filter_entries(self, keyword: str):
        if not keyword:
            self._render_groups(self._raw_entries)
            return

        def match(item: dict, kw: str) -> bool:
            title = str(item.get('title') or '')
            return kw.lower() in title.lower()

        def filter_tree(nodes: List[dict], kw: str) -> List[dict]:
            result: List[dict] = []
            for node in nodes:
                data = node.get('data')
                if isinstance(data, list):
                    children = filter_tree(data, kw)
                    if children:
                        result.append({**node, 'data': children})
                else:
                    if match(node, kw):
                        result.append(node)
            return result

        self._render_groups(filter_tree(self._raw_entries, keyword))

    def _render_groups(self, entries: List[dict]):
        self._clear_layout(self.verticalLayout_groups)
        if not entries:
            self.verticalLayout_groups.addWidget(self._empty_label("暂无数据"))
            return

        # 第一层作为分组，子层为按钮网格
        for item in entries:
            title = str(item.get('title') or '')
            data = item.get('data')
            if isinstance(data, list):
                group = QGroupBox(title, self.container)
                group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
                group_layout = QVBoxLayout(group)
                group_layout.setContentsMargins(8, 8, 8, 8)
                group_layout.setSpacing(8)
                # 子级可能仍有层级，递归平铺按钮
                content_widget = QWidget(group)
                content_layout = QVBoxLayout(content_widget)
                content_layout.setContentsMargins(0, 0, 0, 0)
                content_layout.setSpacing(6)
                self._build_button_rows(data, content_layout)
                group_layout.addWidget(content_widget)
                self.verticalLayout_groups.addWidget(group)
            else:
                # 第一层就是按钮
                row = QHBoxLayout()
                row.setContentsMargins(0, 0, 0, 0)
                row.setSpacing(6)
                row.addWidget(self._create_nav_button(item))
                row.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
                self.verticalLayout_groups.addLayout(row)

        self.verticalLayout_groups.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def _build_button_rows(self, nodes: List[dict], parent_layout: QVBoxLayout, max_per_row: int = 4):
        row_layout: Optional[QHBoxLayout] = None
        count_in_row = 0
        for node in nodes:
            data = node.get('data')
            if isinstance(data, list):
                # 递归：二级组内再建一个小标题
                sub_title = str(node.get('title') or '')
                subtitle_label = QLabel(sub_title)
                font = QFont()
                font.setPointSize(10)
                font.setBold(True)
                subtitle_label.setFont(font)
                parent_layout.addWidget(subtitle_label)
                sub_container = QWidget()
                sub_v = QVBoxLayout(sub_container)
                sub_v.setContentsMargins(0, 0, 0, 0)
                sub_v.setSpacing(6)
                parent_layout.addWidget(sub_container)
                self._build_button_rows(data, sub_v, max_per_row)
            else:
                if row_layout is None or count_in_row >= max_per_row:
                    if row_layout is not None:
                        row_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
                        parent_layout.addLayout(row_layout)
                    row_layout = QHBoxLayout()
                    row_layout.setContentsMargins(0, 0, 0, 0)
                    row_layout.setSpacing(6)
                    count_in_row = 0
                row_layout.addWidget(self._create_nav_button(node))
                count_in_row += 1

        if row_layout is not None:
            row_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
            parent_layout.addLayout(row_layout)

    def _create_nav_button(self, item: dict) -> QPushButton:
        btn = QPushButton(str(item.get('title') or ''))
        btn.setObjectName(str(item.get('name') or 'nav_item'))
        btn.setMinimumHeight(32)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        btn.clicked.connect(lambda: self._on_nav_clicked(item))
        return btn

    def _on_nav_clicked(self, item: dict):
        # title = 菜单名称
        # data = 数据
        name = item.get('name')
        title = WinManager.translate(item.get('title'))
        type = int(item.get('type'))
        data = item.get('data')

        if type == 1:
            # type 1 = 浏览器跳转链接
            webbrowser.open(data)
        elif type == 2:
            # type  2 = 内置浏览器访问
            if self.checkBox_outer.isChecked():
                webbrowser.open(data)
            else:
                PyQtBrowser.open_browser(data, self)
        elif type == 3:
            # type  3 = 二维码页面
            win = QrCodeShowWin(self, title, data)
            win.show()

    @staticmethod
    def _clear_layout(layout: QVBoxLayout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            sub = item.layout()
            if sub:
                NavWin._clear_sub_layout(sub)

    @staticmethod
    def _clear_sub_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            sub = item.layout()
            if sub:
                NavWin._clear_sub_layout(sub)

    @staticmethod
    def _empty_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #666666;")
        return label

    @staticmethod
    def _get_dynamic_nav_config() -> typing.Any:
        # 先读取网络配置，再进行菜单配置
        response = RequestClient.get_instance().get(GlobalConstants.NAV_API_URL)
        if response.status_code != 200:
            return None
        # 解析JSON响应
        return response.json()