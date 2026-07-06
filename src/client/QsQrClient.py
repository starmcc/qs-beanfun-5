from abc import abstractmethod
from typing import Tuple

from src.models.QrCodeResult import QrCodeResult


class QsQrClient:
    @abstractmethod
    def get_qr_code_image(self) -> QrCodeResult:
        pass

    @abstractmethod
    def verify_qr_code_success(self, result: QrCodeResult) -> int:
        pass

    @abstractmethod
    def login(self, result: QrCodeResult) -> Tuple[bool, str]:
        pass


def get_instance() -> QsQrClient:
    from src.client.impl.QsQrClientImpl import QsQrClientImpl
    return QsQrClientImpl()
