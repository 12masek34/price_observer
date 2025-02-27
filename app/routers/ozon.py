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
from app.services.anser_maker import (
    AnserMaker,
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
    anser_maker = AnserMaker()
    await message.answer(anser_maker.in_progress(OZON))
    ozon_subsciber = OzonSubscriberService(message, session)
    subscription = await ozon_subsciber.subscribe()

    if not subscription:
        await message.answer(anser_maker.error_subscribe())
    else:
        await message.answer(anser_maker.success_subscribe(subscription))
