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

from app.services.answer_maker import (
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
    await message.answer(
        "📢 <b>Я умею отслеживать цены на маркетплейсах!</b> 🔍\n\n"
        "🎯 <b>Доступные платформы:</b>\n"
        "   🟦 OZON\n"
        "   🟣 Wildberries\n"
        "   🟡 Yandex Market\n"
        "   🔄 Остальные в разработке...\n\n"
        "💰 Просто отправь мне <b>ссылку на товар</b>, за ценой которого хочешь следить.\n"
        "📉 Как только цена <b>снизится</b> — я сразу сообщу тебе! 🔔",
        parse_mode="HTML"
    )


@router.message(Command("subscribe"))
async def cmd_subscribe(message: types.Message) -> None:
    log_info(message)
    await message.answer("Пришли мне ссылку товара, за которым надо следить.")


@router.message(Command("list"))
async def cmd_list(message: types.Message, session: AsyncSession) -> None:
    log_info(message)
    subsciber_service = BaseSubscriberService(message, session)
    subscriptions = await subsciber_service.get_list_subscriptions()
    answer_maker = AnserMaker()
    answer = answer_maker.list_subscriptions(subscriptions)
    await message.answer(**answer)


@router.message(Command("delete"))
async def cmd_delte(message: types.Message, session: AsyncSession) -> None:
    log_info(message)
    subsciber_service = BaseSubscriberService(message, session)
    subscriptions = await subsciber_service.get_list_subscriptions()
    answer_maker = AnserMaker()
    answer = answer_maker.list_subscriptions_keyboard(subscriptions)
    await message.answer(**answer)
