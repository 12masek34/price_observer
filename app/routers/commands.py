from aiogram import (
    Router,
    types,
)
from aiogram.filters import (
    Command,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.services.anser_maker import (
    AnserMaker,
)
from app.services.base import (
    BaseSubscriberService,
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
    await message.answer("Пришли мне ссылку товара, за которым надо следить.")


@router.message(Command("list"))
async def cmd_list(message: types.Message, session: AsyncSession) -> None:
    log_info(message)
    subsciber = BaseSubscriberService(message, session)
    subscriptions = await subsciber.get_list_subscriptions()
    anser_maker = AnserMaker()
    answer = anser_maker.list_subscriptions(subscriptions)
    await message.answer(answer)
