from aiogram import (
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    WILDBERRIES,
)
from app.parsers.fabric import (
    fabric_parser,
)
from app.services.base import (
    BaseSubscriberService,
)


class WildberriesSubscriberService(BaseSubscriberService):
    service_name = WILDBERRIES

    def __init__(self, message: types.Message, session: AsyncSession) -> None:
        super().__init__(message, session)
        self.parser = fabric_parser(WILDBERRIES, self.get_url())