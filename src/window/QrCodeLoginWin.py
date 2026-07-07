import logging
from base64 import b64decode
from io import BytesIO

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import QDialog

from src.client import QsQrClient
from src.config.GlobalConfig import GLOBAL_CONFIG
from src.models.QrCodeResult import QrCodeResult
from src.utils import SchedulerManager, BoxPop, WinManager
from src.utils.ThreadPoolManager import get_thread_pool
from src.views.Ui_QrCodeLogin import Ui_QrCodeLogin


class QrCodeLoginWin(QDialog, Ui_QrCodeLogin):
    login_win_event = Signal()
    login_success = Signal()
    refresh_event = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_id = None
        self.movie = None
        self.login_success.connect(self._login_success)
        self.setupUi(self)
        WinManager.set_basic_window(self)
        self.init_ui()

    def init_ui(self):
        self.label_qrCode.mousePressEvent = self.refresh_qrCode
        self.refresh_event.connect(self.refresh_qrCode)
        self.refresh_event.emit()

    def refresh_qrCode(self, event=None):
        self.loaded_loading_gif()

        def __load_qr_code(win):
            if win.task_id:
                SchedulerManager.stop_task(win.task_id)
            return QsQrClient.get_instance().get_qr_code_image()

        def __load_qr_code_result(window, result: QrCodeResult, e):
            if e or not result.status:
                if e:
                    result.msg = "网络错误"
                BoxPop.err(window, result.msg)
                return
            image_data = BytesIO(b64decode(result.qr_image))
            pixmap = QPixmap()
            if pixmap.loadFromData(image_data.getvalue()):
                window.label_qrCode.setPixmap(pixmap)
                window.task_id = SchedulerManager.do_task(window.check_login, 1500, result)

        get_thread_pool().submit_task(__load_qr_code, __load_qr_code_result, self, False, win=self)

    def check_login(self, task_id, result: QrCodeResult):
        status = QsQrClient.get_instance().verify_qr_code_success(result)
        if status == 1:
            self.task_id = None
            SchedulerManager.stop_task(task_id)
            # 状态验证成功，已扫码！
            ok, token = QsQrClient.get_instance().login(result)
            if not ok:
                return
            # 登录成功
            logging.info('二维码登录成功!')
            GLOBAL_CONFIG.bf_web_token = token
            self.login_success.emit()

    def loaded_loading_gif(self):
        self.movie = QMovie(":/images/qrLoading")
        self.label_qrCode.setMovie(self.movie)
        self.movie.start()

    def _login_success(self):
        self.close()
        self.login_win_event.emit()

    def closeEvent(self, event):
        """确保所有资源正确清理"""
        # 停止定时器任务
        if self.task_id:
            SchedulerManager.stop_task(self.task_id)
            self.task_id = None

        # 停止动画
        if hasattr(self, 'movie') and self.movie:
            self.movie.stop()
            self.movie = None

        super().closeEvent(event)