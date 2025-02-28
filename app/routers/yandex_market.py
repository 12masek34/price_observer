from aiogram import (
    F,
    Router,
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    YANDEX_MARKET,
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


@router.message(F.text.lower().contains("https") & F.text.lower().contains("market.yandex"))
async def yandx_market(message: types.Message, session: AsyncSession) -> None:
    log_info(message, YANDEX_MARKET)
    await message.answer(answer_maker.in_progress(YANDEX_MARKET))
    price_checker = PriceChecker(message.bot, session)
    await price_checker.create_subscribe(message, session, YANDEX_MARKET)
