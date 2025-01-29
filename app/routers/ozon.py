from aiogram import (
    F,
    Router,
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    OZON,
)
from app.services.ozon import (
    OzonSubscriberService,
)
from app.utils.logging import (
    log_info,
)


router = Router()


@router.message(F.text.lower().contains("https") & F.text.lower().contains("ozon"))
async def ozon(message: types.Message, session: AsyncSession) -> None:
    log_info(message, OZON)
    ozon_subsciber = OzonSubscriberService(message, session)
    subscription = await ozon_subsciber.subscribe()

    await message.answer(f"Подписался на \n\n {subscription.product.name}\n\nЦена {subscription.product.price}₽")
