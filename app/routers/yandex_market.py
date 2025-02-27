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
from app.services.anser_maker import (
    AnserMaker,
)
from app.services.yandex_market import (
    YandexMarketSubscriberService,
)
from app.utils.logging import (
    log_info,
)


router = Router()


@router.message(F.text.lower().contains("https") & F.text.lower().contains("market.yandex"))
async def yandx_market(message: types.Message, session: AsyncSession) -> None:
    log_info(message, YANDEX_MARKET)
    anser_maker = AnserMaker()
    await message.answer(anser_maker.in_progress(YANDEX_MARKET))
    yandex_market_subsciber = YandexMarketSubscriberService(message, session)
    subscription = await yandex_market_subsciber.subscribe()

    if not subscription:
        await message.answer(anser_maker.error_subscribe())
    else:
        await message.answer(anser_maker.success_subscribe(subscription))
