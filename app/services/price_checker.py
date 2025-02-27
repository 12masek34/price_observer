import asyncio
from decimal import (
    Decimal,
)
from typing import (
    Sequence,
)

from aiogram import (
    Bot,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
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


class PriceChecker:

    def __init__(self, bot: Bot, session: async_sessionmaker[AsyncSession]) -> None:
        self.bot = bot
        self.session = session()
        self.subscribe_repository = SubscriptionRepository(self.session)
        self.price_history_repository = PriceHistoryRepository(self.session)

    async def check_by_delay(self):
        while True:
            subscriptions = await self.get_subscriptions()
            for subscription in subscriptions:
                log.info(f"{subscription.id=} {subscription.service_name=} {subscription.product.name=}")
                parser = fabric_parser(subscription.service_name, subscription.url)
                product_data = await parser.parse()

                if not product_data:
                    log.error(
                        f"Не удалось спарсить {subscription.id=} "
                        f"{subscription.service_name=} {subscription.product.name=}"
                    )
                    continue

                log.info(f"{product_data.name=} {product_data.price}")
                new_price_history = await self.price_history_repository.create(subscription, product_data.price)

                if not new_price_history:
                    continue

                min_price = self.get_min_price(subscription)

                if new_price_history.price < min_price:
                    await self.notify_user(subscription, new_price_history, min_price)

            await asyncio.sleep(DELAY_BY_PRICE_CHECK)

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
