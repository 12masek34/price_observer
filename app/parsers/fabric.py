from app.config.settings import (
    OZON,
    WILDBERRIES,
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


def fabric_parser(name: str, *args, **kwargs) -> BaseParser | None:
    if name == OZON:
        parser = OzonParser(*args, **kwargs)
    elif name == WILDBERRIES:
        parser = WildberriesParser(*args, **kwargs)
    else:
        parser = None

    return parser
