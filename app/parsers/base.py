from pyvirtualdisplay import (
    Display,
)


class BaseParser:
    def __init__(self, url: str) -> None:
        self.display = Display(visible=False, size=(1920, 1080), backend="xvfb")
        self.url = url
        self.tab = None
