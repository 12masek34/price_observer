from app.parsers.base import (
    BaseParser,
)


class OzonParser(BaseParser):
    name_product_xpath = ["@data-widget=webProductHeading"]
    price_product_xpath = ["@data-widget=webPrice"]
    price_re = r"\d+"

    def __init__(self, url: str) -> None:
        super().__init__(url)
