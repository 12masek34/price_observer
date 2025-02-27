from app.config.settings import (
    OZON,
    WILDBERRIES,
    YANDEX_MARKET,
)
from app.parsers.base import (
    BaseParser,
)
from app.parsers.ozon import (
    OzonParser,
)
from app.parsers.wildberries import (
    WildberriesParser,
)
from app.parsers.yandex_market import (
    YandexMarketParser,
)


def fabric_parser(name: str, *args, **kwargs) -> BaseParser | None:
    if name == OZON:
        parser = OzonParser(*args, **kwargs)
    elif name == WILDBERRIES:
        parser = WildberriesParser(*args, **kwargs)
    elif name == YANDEX_MARKET:
        parser = YandexMarketParser(*args, **kwargs)
    else:
        parser = None

    return parser
