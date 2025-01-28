import re

from aiogram import (
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.repositories.product import (
    ProductRepository,
)
from app.database.repositories.subscribe import (
    SubscriptionRepository,
)
from app.utils.base import (
    rgetattr,
)


class BaseSubscriberService:

    def __init__(self, message: types.Message, session: AsyncSession) -> None:
        self.message = message
        self.subscribe_repository = SubscriptionRepository(session)
        self.product_repository = ProductRepository(session)

    def get_url(self) -> str:
        if not self.message.text:
            return ""

        url_pattern = re.compile(r"https?://[^\s]+")
        match = url_pattern.search(self.message.text)

        return match.group(0) if match else ""

    def get_user_id(self) -> int:
        return rgetattr(self.message, "from_user.id")

    def get_chat_id(self) -> int:
        return rgetattr(self.message, "chat.id")

    def get_user_name(self) -> str:
        return rgetattr(self.message, "from_user.username")
