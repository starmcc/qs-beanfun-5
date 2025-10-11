from typing import Tuple

from src.plugins.Plugins import Plugins
from src.utils import BaseTools


class LocaleRemulator(Plugins):
    def __init__(self):
        super().__init__()
        self.plugin_name = 'LocaleRemulator'
        self.extend = 'e9cda936-6fba-45fd-8772-d3968eda82b7'
        self.version = '1.6.0'
        self.files: Tuple[str, ...] = (
            'LRHookx32.dll', 'LRHookx64.dll', 'LRProc.exe', 'LRSubMenus.dll',  'LRConfig.xml'
        )

    def build_LRProc_cmd(self):
        path = BaseTools.build_path(rf'plugins\{self.plugin_name}\LRProc.exe')
        return rf'"{path}" {self.extend} '