from aiogram import (
    types,
)

from app.config.settings import (
    log,
)
from app.utils.base import (
    rgetattr,
)


def log_info(message: types.Message | types.CallbackQuery, log_message: str = "") -> None:
        user_id = rgetattr(message, "from_user.id", "")
        user_name = rgetattr(message, "from_user.username", "")
        chat_id = rgetattr(message, "chat.id", "")
        chat_instance = rgetattr(message, "chat_instance", "")
        log.info(
            f"\n{user_id=}\n"
            f"{user_name=}\n"
            f"{chat_id=}\n"
            f"{chat_instance=}\n"
            f"{log_message=}"
        )
