from typing import Any, Dict, List, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QGroupBox, QHBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from src.utils import WinManager
from src.views.Ui_Nav import Ui_Nav


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

    def _load_entries(self):
        # 直接复用原“便捷导航”的获取逻辑
        loader = _MenuLoader(self)
        entry, err = loader.fetch_nav_config()
        if err:
            # 简单提示，沿用全局样式
            self.lineEdit_search.setPlaceholderText(str(err))
            self._raw_entries = []
        else:
            self._raw_entries = entry or []
        self._render_groups(self._raw_entries)

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
                group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
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
                row.addItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
                self.verticalLayout_groups.addLayout(row)

        self.verticalLayout_groups.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

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
                        row_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
                        parent_layout.addLayout(row_layout)
                    row_layout = QHBoxLayout()
                    row_layout.setContentsMargins(0, 0, 0, 0)
                    row_layout.setSpacing(6)
                    count_in_row = 0
                row_layout.addWidget(self._create_nav_button(node))
                count_in_row += 1

        if row_layout is not None:
            row_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
            parent_layout.addLayout(row_layout)

    def _create_nav_button(self, item: dict) -> QPushButton:
        btn = QPushButton(str(item.get('title') or ''))
        btn.setObjectName(str(item.get('name') or 'nav_item'))
        btn.setMinimumHeight(32)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        btn.clicked.connect(lambda: self._on_nav_clicked(item))
        return btn

    def _on_nav_clicked(self, item: dict):
        # 与原动态菜单一致：type 1 外部浏览器; 2 内置浏览器; 3 二维码窗口
        from src.utils.MenuManager import __build_dynamic_menu
        # 复用里面的触发逻辑，构建一个虚拟菜单承载 QAction 并触发一次
        from PyQt5.QtWidgets import QMenu
        menu = QMenu(self)
        # 构造一个最小可用的“菜单节点”让 __build_dynamic_menu 附加行为
        entry = [item]
        __build_dynamic_menu(self, entry, menu)
        actions = menu.actions()
        if actions:
            actions[0].trigger()

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
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #666666;")
        return label


# 为与 MenuManager 的获取逻辑对齐，封装一个轻量加载器
class _MenuLoader:
    def __init__(self, window):
        self.window = window

    def fetch_nav_config(self):
        try:
            from src.utils.MenuManager import __get_dynamic_menu_config
            data = __get_dynamic_menu_config()
            return data, None
        except Exception as e:
            return None, e

