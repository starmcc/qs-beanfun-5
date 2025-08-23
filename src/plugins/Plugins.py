from typing import Tuple


class Plugins:

    def __init__(self):
        super().__init__()
        self.plugin_name: str = ''
        self.files: Tuple[str, ...] = ()
