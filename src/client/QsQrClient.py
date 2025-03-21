from abc import abstractmethod

from src.models.QrCodeResult import QrCodeResult


class QsQrClient:
    @abstractmethod
    def get_qr_code_image(self) -> QrCodeResult:
        pass

    @abstractmethod
    def verify_qr_code_success(self, str_encrypt_data: str) -> int:
        pass

    @abstractmethod
    def login(self, session_key: str) -> (bool, str):
        pass


def get_instance() -> QsQrClient:
    from src.client.impl.QsQrClientImpl import QsQrClientImpl
    return QsQrClientImpl()
