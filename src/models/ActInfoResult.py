from src.models.Account import Account


class ActInfoResult:

    def __init__(self):
        self.cert_status = False
        self.accounts: list[Account] = []
        self.auth_cert = True
        # 最大可创建账号数量（None 表示未限制或无法解析）
        self.account_limit = None
