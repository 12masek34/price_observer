from app.database.models.subscription import (
    Subscription,
)
from app.parsers.base import (
    BaseParser,
)

class YandexMarketParser(BaseParser):
    name_product_xpath = ["@data-auto=productCardTitle"]
    price_product_xpath = ["@data-auto=snippet-price-current", "@data-auto=price-value"]
    price_re = r"\d+"

    def __init__(self, subscription: Subscription | None = None, url: str | None = None) -> None:
        super().__init__(subscription=subscription, url=url)