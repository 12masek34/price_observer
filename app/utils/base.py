from functools import (
    reduce,
)
from typing import (
    Any,
)


def rgetattr(obj: object, attr: str, default: Any = None) -> Any:
    try:
        value = reduce(lambda o, a: getattr(o, a), [obj] + attr.split("."))
    except AttributeError:
        return default or ""

    if value is None:
        return default or ""

    return value
