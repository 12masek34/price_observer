from app.database.models.subscription import (
    Subscription,
)
from app.parsers.base import (
    BaseParser,
)


class OzonParser(BaseParser):
    name_product_xpath = ["@data-widget=webProductHeading"]
    price_product_xpath = ["@data-widget=webPrice"]
    price_re = r"\d+"

    def __init__(self, subscription: Subscription | None = None, url: str | None = None) -> None:
        super().__init__(subscription=subscription, url=url)
