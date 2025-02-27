from app.parsers.base import (
    BaseParser,
)


class YandexMarketParser(BaseParser):
    name_product_xpath = ["@data-auto=productCardTitle"]
    price_product_xpath = ["@data-auto=snippet-price-current", "@data-auto=price-value"]
    price_re = r"\d+"

    def __init__(self, url: str) -> None:
        super().__init__(url)
