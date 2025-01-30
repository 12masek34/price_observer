from app.parsers.base import (
    BaseParser,
)


class OzonParser(BaseParser):
    name_product_xpath = ".lt7_27 tsHeadline550Medium"
    price_product_xpath = ".l6s_27 sl4_27"

    def __init__(self, url: str) -> None:
        super().__init__(url)
