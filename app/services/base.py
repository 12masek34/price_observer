import re
from concurrent.futures import (
    ProcessPoolExecutor,
)
from typing import (
    Sequence,
    Type,
)

from aiogram import (
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    DELETE_SUBSCRIPTION_PREFIX,
    OZON,
    WILDBERRIES,
    YANDEX_MARKET,
    log,
)
from app.database.models.subscription import (
    Subscription,
)
from app.database.repositories.product import (
    ProductRepository,
)
from app.database.repositories.subscribe import (
    SubscriptionRepository,
)
from app.utils.base import (
    rgetattr,
)


class BaseSubscriberService:

    def __init__(self, message: types.Message | types.CallbackQuery, session: AsyncSession) -> None:
        self.message = message
        self.subscribe_repository = SubscriptionRepository(session)
        self.product_repository = ProductRepository(session)
        self.parser = None
        self.process_pool = ProcessPoolExecutor()

    async def subscribe(self) -> Subscription | None:
        product_data = await self.parser.parse_to_thered()

        if not product_data.price or not product_data.name:
            log.error(f"Не удалось спарсить")
            return

        product = await self.product_repository.create(product_data.name, product_data.price)
        subscription = await self.subscribe_repository.create(
            self.get_user_id(),
            self.get_chat_id(),
            product.id,
            self.get_user_name(),
            self.get_url(),
            self.service_name,
        )

        return subscription

    async def get_list_subscriptions(self) -> Sequence[Subscription]:
        return await self.subscribe_repository.get_subscrptions_by_user_id(self.message.from_user.id)

    async def delete_subscription_by_button(self):
        subscription_id = int(self.message.data.replace(DELETE_SUBSCRIPTION_PREFIX, ""))
        return await self.subscribe_repository.delete_by_id(subscription_id)

    def get_url(self) -> str:
        if not self.message.text:
            return ""

        url_pattern = re.compile(r"https?://[^\s]+")
        match = url_pattern.search(self.message.text)

        return match.group(0) if match else ""

    def get_user_id(self) -> int:
        return rgetattr(self.message, "from_user.id")

    def get_chat_id(self) -> int:
        return rgetattr(self.message, "chat.id")

    def get_user_name(self) -> str:
        return rgetattr(self.message, "from_user.username")


def fabric_subscriber(service_name: str) -> Type[BaseSubscriberService]:
    if service_name == OZON:
        from app.services.ozon import OzonSubscriberService
        return OzonSubscriberService
    elif service_name == WILDBERRIES:
        from app.services.wildberries import WildberriesSubscriberService
        return WildberriesSubscriberService
    elif service_name == YANDEX_MARKET:
        from app.services.yandex_market import YandexMarketSubscriberService
        return YandexMarketSubscriberService
    else:
        raise
