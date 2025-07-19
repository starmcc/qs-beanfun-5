class TitleBarConfig:
    def __init__(self, title="", min_btn=True, max_btn=False, close_btn=True):
        self.title: str = title
        self.min_btn: bool = min_btn
        self.max_btn: bool = max_btn
        self.close_btn: bool = close_btn
