from app.parsers.base import (
    BaseParser,
)


class WildberriesParser(BaseParser):
    name_product_xpath = [".product-page__title"]
    price_product_xpath = [".price-block__wallet-price red-price", ".price-block__wallet-price"]


    def __init__(self, url: str) -> None:
        super().__init__(url)
