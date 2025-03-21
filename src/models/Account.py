class Account:

    def __init__(self):
        self.id = None
        self.status = False
        self.sn = None
        self.name = None
        self.create_time = None
        self.auth_type = None
        self.dynamic_pwd: str = ''
