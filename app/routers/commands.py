from aiogram import (
    F,
    Router,
    types,
)
from aiogram.filters import (
    Command,
)

router = Router()


@router.message(Command("start"))
@router.message(F.text.lower() == "start")
async def cmd_start(message: types.Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    chat_id = message.chat.id
    await message.answer(f"привет {user_name}")
