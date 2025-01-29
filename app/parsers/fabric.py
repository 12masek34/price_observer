from app.config.settings import (
    OZON,
)
from app.parsers.base import (
    BaseParser,
)
from app.parsers.ozon import (
    OzonParser,
)


def fabric_parser(name: str, *args, **kwargs) -> BaseParser | None:
    if name == OZON:
        parser = OzonParser(*args, **kwargs)
    else:
        parser = None

    return parser
