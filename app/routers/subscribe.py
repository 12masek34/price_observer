from aiogram import (
    F,
    Router,
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    DELETE_SUBSCRIPTION_PREFIX,
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


@router.callback_query(F.data.startswith(DELETE_SUBSCRIPTION_PREFIX))
async def delete_subscription(callback_query: types.CallbackQuery, session: AsyncSession) -> None:
    log_info(callback_query)
    subsciber_service = BaseSubscriberService(callback_query, session)
    delete_subscription = await subsciber_service.delete_subscription_by_button()
    anser_maker = AnserMaker()
    subscriptions = await subsciber_service.get_list_subscriptions()
    answer = anser_maker.list_subscriptions_keyboard([subscription for subscription in subscriptions if subscription.id != delete_subscription.id])

    await callback_query.message.edit_reply_markup(**answer)
