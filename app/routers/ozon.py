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
from app.services.answer_maker import (
    answer_maker,
)
from app.services.price_checker import (
    PriceChecker,
)
from app.utils.logging import (
    log_info,
)


router = Router()


@router.message(F.text.lower().contains("https") & F.text.lower().contains("ozon"))
async def ozon(message: types.Message, session: AsyncSession) -> None:
    log_info(message, OZON)
    await message.answer(answer_maker.in_progress(OZON))
    price_checker = PriceChecker(message.bot, session)
    await price_checker.create_subscribe(message, session, OZON)
