from app.parsers.base import (
    BaseParser,
)


class OzonParser(BaseParser):
    name_product_xpath = [".t9l_27 tsHeadline550Medium"]
    price_product_xpath = [".ls9_27 l7s_27"]

    def __init__(self, url: str) -> None:
        super().__init__(url)
