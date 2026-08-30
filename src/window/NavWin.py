import json
import logging
import typing
import webbrowser
from typing import Any, Dict, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QGroupBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from src.client import RequestClient
from src.config import Config
from src.config.GlobalConfig import GlobalConstants, LANGUAGE
from src.utils import WinManager
from src.config.I18n import I18N
from src.utils.ThreadPoolManager import get_thread_pool
from src.views.UI_Nav import Ui_Nav
from src.window import CustomToolTipWin
from src.components import PyQtBrowser
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
        I18N.language_changed.connect(lambda _language: self._refresh_entries())

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
            if Config.language() == LANGUAGE.EN.value:
                en = str(item.get('en') or '')
                if en:
                    return kw.lower() in en.lower()
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

    def _refresh_entries(self):
        self._filter_entries(self.lineEdit_search.text())

    def _localized(self, item: dict) -> str:
        """根据当前语言返回显示文本：英文时优先使用 en 字段，否则回退 title。"""
        title = str(item.get('title') or '')
        if Config.language() == LANGUAGE.EN.value:
            en = str(item.get('en') or '')
            if en:
                return en
        return WinManager.translate(title)

    def _render_groups(self, entries: List[dict]):
        self._clear_layout(self.verticalLayout_groups)
        if not entries:
            self.verticalLayout_groups.addWidget(self._empty_label("暂无数据"))
            return

        # 第一层作为分组，子层为按钮网格
        for item in entries:
            data = item.get('data')
            if isinstance(data, list):
                group = QGroupBox(self._localized(item), self.container)
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
                subtitle_label = QLabel(self._localized(node))
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
        btn = QPushButton(self._localized(item))
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
        title = self._localized(item)
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
        label = QLabel(WinManager.translate(text))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #666666;")
        return label

    @staticmethod
    def _get_dynamic_nav_config() -> typing.Any:
        a =  """
        [
    {
        "name": "nav_tools",
        "en": "Navigation Tools",
        "type": 0,
        "title": "实用工具",
        "data": [
            {
                "name": "tools_maple_kit",
                "en": "MapleKit",
                "type": 1,
                "title": "MapleKit",
                "data": "https://maple-kit.com/"
            },
            {
                "name": "tools_hexa",
                "en": "Hexa Calculator",
                "type": 2,
                "title": "Hexa计算器",
                "data": "https://starmcc.github.io/MapleStoryCoreCalc/"
            },
            {
                "name": "tools_star",
                "en": "Star Force Simulator",
                "type": 2,
                "title": "星力模拟器",
                "data": "https://maplehexa.cisyy.cc/starforceEmulator/"
            },
            {
                "name": "tools_all_tools",
                "en": "MapleStory Toolbox",
                "type": 2,
                "title": "枫之谷小工具",
                "data": "https://mstoolbox.netlify.app/"
            },
            {
                "name": "tools_union",
                "en": "Legion Solver",
                "type": 2,
                "title": "联盟摆放模拟器",
                "data": "https://xenogents.github.io/LegionSolver/"
            },
            {
                "name": "tools_paper_dolls",
                "en": "Open‑Source Paper Doll System",
                "type": 1,
                "title": "开源纸娃娃系统",
                "data": "https://github.com/Elem8100/MapleNecrocer"
            },
            {
                "name": "tools_exchange",
                "en": "Currency Converter",
                "type": 2,
                "title": "汇率换算",
                "data": "https://zh.coinmill.com/CNY_calculator.html"
            }
        ]
    },
    {
        "name": "nav_beanfun",
        "en": "Beanfun Official Links",
        "type": 0,
        "title": "新枫之谷官方链接",
        "data": [
            {
                "name": "beanfun_recharge",
                "en": "(Taobao) GASH Card Purchase",
                "type": 3,
                "title": "(淘宝)GASH点卡购买",
                "data": "shturl.cc/lEPZTGfOKaGHrLBoJqmGwtUNGbGQzNq9eOLKGircQ9IbxH6aCwdsaGdLrkZs2"
            },
            {
                "name": "beanfun_maplestory_classic",
                "en": "MapleStory Classic Official Site",
                "type": 1,
                "title": "新枫之谷经典版官网",
                "data": "https://maplestoryclassic.beanfun.com/Main"
            },
            {
                "name": "beanfun_hk",
                "en": "Beanfun Hong Kong",
                "type": 1,
                "title": "香港橘子",
                "data": "https://bfweb.hk.beanfun.com/"
            },
            {
                "name": "beanfun_tw",
                "en": "Beanfun Taiwan",
                "type": 1,
                "title": "台湾橘子",
                "data": "https://tw.beanfun.com/"
            },
            {
                "name": "beanfun_maplestory",
                "en": "MapleStory TW Official Site",
                "type": 1,
                "title": "新枫之谷官网",
                "data": "https://maplestory.beanfun.com/main"
            },
            {
                "name": "beanfun_facebook",
                "en": "(Facebook) Taiwan Official Fanpage",
                "type": 1,
                "title": "(脸书)台湾官方粉丝团",
                "data": "https://www.facebook.com/www.maplestory.msfans.com.tw"
            },
            {
                "name": "beanfun_intagram",
                "en": "(Instagram) MapleStory TW",
                "type": 1,
                "title": "(IG/INS)新枫之谷",
                "data": "https://www.instagram.com/maplestory_tw/"
            },
            {
                "name": "beanfun_blacklist",
                "en": "MapleStory Ban List",
                "type": 1,
                "title": "枫谷官方封神榜",
                "data": "https://maplestory.beanfun.com/blacklist"
            }
        ]
    },
    {
        "name": "nav_cms",
        "en": "Community & Forums",
        "type": 0,
        "title": "社区论坛",
        "data": [
            {
                "name": "cms_baidu_beanfun",
                "en": "Beanfun Tieba Forum",
                "type": 1,
                "title": "Beanfun贴吧",
                "data": "https://tieba.baidu.com/f?kw=beanfun"
            },
            {
                "name": "cms_baidu_maplestory",
                "en": "MapleStory Tieba Forum",
                "type": 1,
                "title": "新枫之谷贴吧",
                "data": "https://tieba.baidu.com/f?kw=%E6%96%B0%E6%9E%AB%E4%B9%8B%E8%B0%B7"
            },
            {
                "name": "cms_bahamute",
                "en": "Bahamut Forum",
                "type": 1,
                "title": "巴哈姆特",
                "data": "https://forum.gamer.com.tw/B.php?bsn=7650"
            },
            {
                "name": "cms_nga",
                "en": "NGA MapleStory Forum",
                "type": 1,
                "title": "NGA冒险岛论坛",
                "data": "https://bbs.nga.cn/thread.php?fid=707"
            }
        ]
    },
    {
        "name": "nav_blogMaster",
        "en": "Content Creators",
        "type": 0,
        "title": "视频博主",
        "data": [
            {
                "name": "blogMaster_xiaomeng",
                "en": "(Bilibili‑TMS) Childhood Dream",
                "type": 1,
                "title": "(B站‑TMS)童年小梦",
                "data": "https://space.bilibili.com/391919722"
            },
            {
                "name": "blogMaster_mofu",
                "en": "(Bilibili‑CMS) Mofu",
                "type": 1,
                "title": "(B站‑CMS)魔符",
                "data": "https://space.bilibili.com/270041969"
            },
            {
                "name": "blogMaster_huoguo",
                "en": "(Bilibili‑CMS) Hotpot",
                "type": 1,
                "title": "(B站‑CMS)火锅",
                "data": "https://space.bilibili.com/1784563171"
            },
            {
                "name": "blogMaster_reqingTv",
                "en": "(Bilibili‑CMS) ReqingTV",
                "type": 1,
                "title": "(B站‑CMS)热情TV",
                "data": "https://space.bilibili.com/295598050"
            }
        ]
    }
]

        """
        return json.loads(a)
        # 先读取网络配置，再进行菜单配置
        response = RequestClient.get_instance().get(GlobalConstants.NAV_API_URL)
        if response.status_code != 200:
            return None
        # 解析JSON响应
        return response.json()