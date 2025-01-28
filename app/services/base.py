import re

from aiogram import (
    types,
)

from app.database.repositories.subscribe import (
    SubscribeRepository,
)
from app.utils.base import (
    rgetattr,
)


class BaseSubscriberService:

    def __init__(self, message: types.Message) -> None:
        self.message = message
        self.subscribe_repository = SubscribeRepository()

    def get_url(self) -> str:
        if not self.message.text:
            return ""

        url_pattern = re.compile(r"https?://[^\s]+")
        match = url_pattern.search(self.message.text)

        return match.group(0) if match else ""

    def get_user_id(self) -> int | None:
        return rgetattr(self.message, "from_user.id")

    def get_chat_id(self) -> int | None:
        return rgetattr(self.message, "chat.id")

    def get_user_name(self) -> str | None:
        return rgetattr(self.message, "from_user.username")
