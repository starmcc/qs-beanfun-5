from typing import Optional, Callable, List


class CustomMenu:
    def __init__(
            self,
            name: str,
            title: str,
            handler: Optional[Callable] = None,
            children: Optional[List["CustomMenu"]] = None
    ):
        super().__init__()
        self.name = name
        self.title = title
        self.handler = handler
        self.children = children or []
