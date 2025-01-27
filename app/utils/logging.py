from aiogram import (
    types,
)

from app.config.settings import (
    log,
)
from app.utils.base import (
    rgetattr,
)


def log_info(message: types.Message, log_message: str = "") -> None:
        user_id = rgetattr(message, "from_user.id")
        user_name = rgetattr(message, "from_user.username")
        first_name = rgetattr(message, "from_user.first_name")
        chat_id = rgetattr(message, "chat.id")
        log.info(
            f"\n{user_id=}\n"
            f"{user_name=}\n"
            f"{first_name=}\n"
            f"{chat_id=}\n"
            f"{log_message=}"
        )
