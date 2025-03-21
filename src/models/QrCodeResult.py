class QrCodeResult:
    def __init__(self, status=False):
        super().__init__()
        self.status = status
        self.msg = ''
        self.session_key: str = ''
        self.str_encrypt_data: str = ''
        self.str_encrypt_bcdd_data: str = ''
        self.qr_image: bytes = bytes()
