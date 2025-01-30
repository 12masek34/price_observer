import asyncio
import re
from concurrent.futures import (
    ProcessPoolExecutor,
)
from typing import (
    Sequence,
)

from aiogram import (
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    DELETE_SUBSCRIPTION_PREFIX,
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

    @staticmethod
    def parse_sync(parser):
        return asyncio.run(parser.parse())

    async def subscribe(self) -> Subscription | None:
        loop = asyncio.get_running_loop()
        product_data = await loop.run_in_executor(self.process_pool, self.parse_sync, self.parser)

        if not product_data:
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
