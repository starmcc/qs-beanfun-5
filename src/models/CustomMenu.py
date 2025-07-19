from typing import Optional, Callable, List


class CustomMenu:
    def __init__(
            self,
            menu_id: int,
            title: str,
            handler: Optional[Callable] = None,
            children: Optional[List["CustomMenu"]] = None
    ):
        self.menu_id = menu_id
        self.title = title
        self.handler = handler
        self.children = children or []
