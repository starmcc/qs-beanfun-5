from io import BytesIO

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QDialog

from src.client import RequestClient
from src.models.QrCodeResult import QrCodeResult
from src.utils import WinManager, BoxPop
from src.utils.ThreadPoolManager import get_thread_pool
from src.views.Ui_QrCodeShow import Ui_QrCodeShow


class QrCodeShowWin(QDialog, Ui_QrCodeShow):
    refresh_event = pyqtSignal()

    def __init__(self, parent, title: str, data: str):
        super().__init__(parent)
        self.data = data
        self.setupUi(self)
        WinManager.set_basic_window(self)
        self.setWindowTitle(title)
        self.init_ui()

    def init_ui(self):
        self.label_qrCode.mousePressEvent = self.refresh_qrCode
        self.refresh_event.connect(self.refresh_qrCode)
        self.refresh_event.emit()

    def refresh_qrCode(self, event=None):
        self.loaded_loading_gif()

        def __load_qr_code():
            qr_code_result = QrCodeResult()
            rsp = RequestClient.get_instance().get(self.data)
            # 检查HTTP响应状态码
            if rsp.status_code != 200:
                qr_code_result.msg = '获取二维码失败,错误代码[0]'
                return qr_code_result
            qr_code_result.qr_image = rsp.content
            qr_code_result.status = True
            return qr_code_result

        def __load_qr_code_result(window, result: QrCodeResult, e):
            if e or not result.status:
                if e:
                    result.msg = "网络错误"
                BoxPop.err(self, result.msg)
                return
            image_data = BytesIO(result.qr_image)
            pixmap = QPixmap()
            if pixmap.loadFromData(image_data.getvalue()):
                self.label_qrCode.setPixmap(pixmap)

        get_thread_pool().submit_task(__load_qr_code, __load_qr_code_result, self, False)

    def loaded_loading_gif(self):
        movie = QMovie(":/images/qrLoading")
        self.label_qrCode.setMovie(movie)
        movie.start()
