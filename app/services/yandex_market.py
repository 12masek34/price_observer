from aiogram import (
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    YANDEX_MARKET,
)
from app.parsers.fabric import (
    fabric_parser,
)
from app.services.base import (
    BaseSubscriberService,
)


class YandexMarketSubscriberService(BaseSubscriberService):
    service_name = YANDEX_MARKET

    def __init__(self, message: types.Message, session: AsyncSession) -> None:
        super().__init__(message, session)
        self.parser = fabric_parser(YANDEX_MARKET, self.get_url())
