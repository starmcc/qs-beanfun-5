from typing import Tuple


class Plugins:

    def __init__(self):
        super().__init__()
        self.plugin_name: str = ''
        self.extend = ''
        self.version = ''
        self.files: Tuple[str, ...] = ()
