class LoginRecord:
    CALLBACK_TYPE_TW_INTERMEDIATE_LOGIN = 1

    def __init__(self, status: bool, message: str):
        super().__init__()
        self.skey = ''
        self.status = status
        self.daul_status = False
        self.adv_status = False
        self.content = ''
        self.message = message
        self.dual_code = ''
        self.auth_key = ''
        self.bfWebToken = ''
        self.location = ''
        self.lt = ''
        self.intermediate_login = False
