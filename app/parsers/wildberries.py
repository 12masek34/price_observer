from app.database.models.subscription import (
    Subscription,
)
from app.parsers.base import (
    BaseParser,
)


class WildberriesParser(BaseParser):
    name_product_xpath = [".product-page__title"]
    price_product_xpath = [".price-block__wallet-price red-price", ".price-block__wallet-price"]
    price_re = r"\d{1,3}(?:\s\d{3})*"

    def __init__(self, subscription: Subscription | None = None, url: str | None = None) -> None:
        super().__init__(subscription=subscription, url=url)