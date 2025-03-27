import logging
from io import BytesIO

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QDialog

from src.client import QsQrClient
from src.config.GlobalConfig import GLOBAL_CONFIG
from src.models.QrCodeResult import QrCodeResult
from src.utils import BaseTools, SchedulerManager, BoxPop
from src.utils.ThreadTools import CustomThread
from src.views.Ui_QrCodeLogin import Ui_QrCodeLogin


class QrCodeLoginWin(QDialog, Ui_QrCodeLogin):
    login_win_event = pyqtSignal()
    login_success = pyqtSignal()
    refresh_event = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_id = None
        self.login_success.connect(self._login_success)
        self.setupUi(self)
        BaseTools.set_basic_window(self)
        self.init_ui()

    def init_ui(self):
        self.label_qrCode.mousePressEvent = self.refresh_qrCode
        self.refresh_event.connect(self.refresh_qrCode)
        self.refresh_event.emit()

    def refresh_qrCode(self, event=None):
        self.loaded_loading_gif()

        def load_qr_code():
            if self.task_id:
                SchedulerManager.stop_task(self.task_id)
            return QsQrClient.get_instance().get_qr_code_image()

        def load_qr_code_result(result: QrCodeResult):
            if not result.status:
                BoxPop.err(self, result.msg)
                return
            image_data = BytesIO(result.qr_image)
            pixmap = QPixmap()
            if pixmap.loadFromData(image_data.getvalue()):
                self.label_qrCode.setPixmap(pixmap)
                self.task_id = SchedulerManager.do_task(self.check_login, 2000, result)

        CustomThread().run_task(load_qr_code, load_qr_code_result)

    def check_login(self, task_id, result: QrCodeResult):
        status = QsQrClient.get_instance().verify_qr_code_success(result.str_encrypt_data)
        if status == 1:
            self.task_id = None
            SchedulerManager.stop_task(task_id)
            # 状态验证成功，已扫码！
            ok, token = QsQrClient.get_instance().login(result.session_key)
            if not ok:
                return
            # 登录成功
            logging.info('二维码登录成功!')
            GLOBAL_CONFIG.bf_web_token = token
            self.login_success.emit()

    def loaded_loading_gif(self):
        movie = QMovie(":/images/qrLoading")
        self.label_qrCode.setMovie(movie)
        movie.start()

    def closeEvent(self, event):
        if self.task_id:
            SchedulerManager.stop_task(self.task_id)
        super().close()

    def _login_success(self):
        self.close()
        self.login_win_event.emit()
