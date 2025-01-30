from aiogram import (
    F,
    Router,
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    WILDBERRIES,
)
from app.services.anser_maker import (
    AnserMaker,
)
from app.services.wildberries import (
    WildberriesSubscriberService,
)
from app.utils.logging import (
    log_info,
)


router = Router()


@router.message(F.text.lower().contains("https") & F.text.lower().contains("wildberries"))
async def wildberries(message: types.Message, session: AsyncSession) -> None:
    log_info(message, WILDBERRIES)
    wildberries_subsciber = WildberriesSubscriberService(message, session)
    subscription = await wildberries_subsciber.subscribe()
    anser_maker = AnserMaker()

    if not subscription:
        await message.answer(anser_maker.error_subscribe())
    else:
        await message.answer(anser_maker.success_subscribe(subscription))