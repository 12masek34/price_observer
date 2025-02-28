from aiogram import (
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    OZON,
)
from app.parsers.fabric import (
    fabric_parser,
)
from app.services.base import (
    BaseSubscriberService,
)


class OzonSubscriberService(BaseSubscriberService):
    service_name = OZON

    def __init__(self, message: types.Message, session: AsyncSession) -> None:
        super().__init__(message, session)
        self.parser = fabric_parser(OZON, url=self.get_url())
