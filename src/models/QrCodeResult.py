class QrCodeResult:
    def __init__(self, status=False):
        super().__init__()
        self.status = status
        self.msg = ''
        self.session_key: str = ''
        self.qr_image: bytes = bytes()
        self.requestVerificationToken: str = ''
