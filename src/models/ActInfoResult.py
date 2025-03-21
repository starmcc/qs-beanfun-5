from src.models.Account import Account


class ActInfoResult:

    def __init__(self):
        self.cert_status = False
        self.new_user = False
        self.accounts: list[Account] = []
        self.auth_cert = True
