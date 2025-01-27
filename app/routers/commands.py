from aiogram import (
    Router,
    types,
)
from aiogram.filters import (
    Command,
)

from app.utils.logging import (
    log_info,
)


router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    log_info(message)
    await message.answer(f"привет \n тут будет описания всего что я умею")


@router.message(Command("subscribe"))
async def cmd_subscribe(message: types.Message) -> None:
    log_info(message)
    await message.answer(f"привет \n тут будет описания всего что я умею")