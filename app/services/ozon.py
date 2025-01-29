from aiogram import (
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.parsers.ozon import (
    OzonParser,
)
from app.services.base import (
    BaseSubscriberService,
)


class OzonSubscriberService(BaseSubscriberService):
    service_name = "OZON"

    def __init__(self, message: types.Message, session: AsyncSession) -> None:
        super().__init__(message, session)
        self.parser = OzonParser(self.get_url())
