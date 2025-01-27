from aiogram import (
    F,
    Router,
    types,
)

from app.utils.logging import (
    log_info,
)
from app.services.ozon import OzonSubsciberService


router = Router()


@router.message(F.text.lower().contains("https") & F.text.lower().contains("ozon"))
async def ozon(message: types.Message) -> None:
    log_info(message, "OZON")
    ozon_subsciber = OzonSubsciberService(message)
    product = ozon_subsciber.subscribe()
    await message.answer(f"Подписался на {product}")
