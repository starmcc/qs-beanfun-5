from typing import Tuple

from src.plugins.Plugins import Plugins


class LocaleRemulator(Plugins):
    def __init__(self):
        super().__init__()
        self.plugin_name = 'LocaleRemulator.zip'
        self.files: Tuple[str, ...] = (
            'LRHookx32.dll', 'LRHookx64.dll', 'LRProc.exe', 'LRSubMenus.dll', 'SharpShell.dll', 'LRConfig.xml'
        )
