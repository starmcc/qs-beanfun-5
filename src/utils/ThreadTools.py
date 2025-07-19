import logging

from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from src.window.LoadMask import LoadMask


class CustomThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, fnc=None):
        super().__init__()
        self.fnc = fnc

    def run(self):
        result = None
        if self.fnc is not None:
            try:
                result = self.fnc()
            except Exception as e:
                logging.error(f"Thread execution error: {e}")
        self.finished.emit(result)

    @staticmethod
    def run_task(fnc=None, re_fnc=None, load_mask: LoadMask = None):
        thread = CustomThread(fnc)

        def __result_fnc(data):
            if re_fnc is not None:
                re_fnc(data)
            if load_mask is not None:
                # 使用deleteLater()确保在UI线程中安全删除
                QTimer.singleShot(0, load_mask.deleteLater)
            # 线程结束后清理
            thread.deleteLater()

        thread.finished.connect(__result_fnc)
        # 线程结束后自动退出
        thread.finished.connect(thread.quit)
        thread.start()
