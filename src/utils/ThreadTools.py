from PyQt5.QtCore import QThread, pyqtSignal

from src.config.GlobalConfig import GLOBAL_CONFIG
from src.window.LoadMask import LoadMask


class CustomThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, fnc=None):
        super().__init__()
        self.fnc = fnc

    def run(self):
        result = None
        if self.fnc is not None:
            result = self.fnc()
        self.finished.emit(result)

    @staticmethod
    def run_task(fnc=None, re_fnc=None, load_mask: LoadMask = None):
        GLOBAL_CONFIG.custom_thread = CustomThread(fnc)

        def __result_fnc(data):
            if re_fnc is not None:
                re_fnc(data)
            if load_mask is not None:
                load_mask.deleteLater()

        GLOBAL_CONFIG.custom_thread.finished.connect(__result_fnc)
        GLOBAL_CONFIG.custom_thread.start()
