import asyncio
from decimal import (
    Decimal,
)
from typing import (
    Sequence,
)

from aiogram import (
    Bot,
    types,
)
from pyvirtualdisplay.display import (
    Display,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    DELAY_BY_PRICE_CHECK,
    log,
)
from app.database.models.price_history import (
    PriceHistory,
)
from app.database.models.subscription import (
    Subscription,
)
from app.database.repositories.price_history import (
    PriceHistoryRepository,
)
from app.database.repositories.subscribe import (
    SubscriptionRepository,
)
from app.parsers.fabric import (
    fabric_parser,
)
from app.services.answer_maker import (
    answer_maker,
)
from app.services.base import (
    fabric_subscriber,
)
class PriceChecker:

    def __init__(self, bot: Bot, session: AsyncSession) -> None:
        self.bot = bot
        self.session = session
        self.subscribe_repository = SubscriptionRepository(self.session)
        self.price_history_repository = PriceHistoryRepository(self.session)
        self.display = Display(visible=False, size=(1920, 1080), backend="xvfb")

    async def check_by_delay(self):
        self.display.start()
        try:
            while True:
                await self.parse_subscriptions()
                await asyncio.sleep(DELAY_BY_PRICE_CHECK)
        finally:
            self.display.stop()

    async def parse_subscriptions(self):
        subscriptions = await self.get_subscriptions()
        tasks = self.make_tasks(subscriptions)

        for task in asyncio.as_completed(tasks):
            product_data = await task

            if not product_data.name or not product_data.price:
                log.error(
                    f"\nНе удалось спарсить\n"
                    f"{product_data.subscription.id=}\n"
                    f"{product_data.subscription.service_name=}\n"
                    f"{product_data.subscription.product.name=}\n"
                )
                continue

            log.info(
                f"\nУспешно спарсил\n"
                f"{product_data.subscription.id=}\n"
                f"{product_data.subscription.service_name=}\n"
                f"{product_data.name=}\n"
                f"{product_data.price=}\n"
            )
            new_price_history = await self.price_history_repository.create(product_data.subscription, product_data.price)

            if not new_price_history:
                log.error(
                    f"\nНе удалось сохранить\n"
                    f"{product_data.name=}\n"
                    f"{product_data.price=}\n"
                )
                continue

            min_price = self.get_min_price(product_data.subscription)

            if new_price_history.price < min_price:
                await self.notify_user(product_data.subscription, new_price_history, min_price)

    def make_tasks(self, subscriptions: Sequence[Subscription]) -> list:
        return [
            asyncio.create_task(fabric_parser(subscription.service_name, subscription=subscription).parse_to_thered())
            for subscription in subscriptions
        ]

    async def get_subscriptions(self) -> Sequence[Subscription]:
        return await self.subscribe_repository.get_all_subscrptions()

    def get_min_price(self, subscription: Subscription) -> Decimal:
        prices = [price_history. price for price_history in subscription.price_history]
        prices.append(subscription.product.price)

        return min(prices)

    async def notify_user(
        self,
        subscription: Subscription,
        new_price_history: PriceHistory,
        min_price: Decimal,
    ) -> None:
        await self.bot.send_message(
            subscription.chat_id,
            f"{subscription.service_name}\n"
            f"📉 Цена на {subscription.product.name} снизилась!\n"
            f"Было: {min_price}₽ → Стало: {new_price_history.price}₽",
        )

    async def create_subscribe(self,message: types.Message, session: AsyncSession, service_name: str) -> None:

        subsciber_class = fabric_subscriber(service_name)
        subscriber = subsciber_class(message, session)
        subscription = await subscriber.subscribe()

        if not subscription:
            await message.answer(answer_maker.error_subscribe())
        else:
            log.info(
                "\nПодписался\n"
                f"{service_name=}\n"
                f"{subscription.product.name=}\n"
                f"{subscription.product.price=}\n"
            )
            await message.answer(answer_maker.success_subscribe(subscription))