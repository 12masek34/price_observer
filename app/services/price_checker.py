import asyncio

from datetime import (
    datetime,
)
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
    OZON,
    WILDBERRIES,
    YANDEX_MARKET,
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

    async def check_by_delay(self) -> None:
        self.display.start()
        start_time = datetime.now()
        while True:
            interval = datetime.now() - start_time

            if interval.total_seconds() > DELAY_BY_PRICE_CHECK:
                start_time = datetime.now()
                subscriptions = await self.get_subscriptions()
                log.info(f"========start parsing count={len(subscriptions)}==========")
                tasks = self.make_tasks(subscriptions)
                try:
                    error_subscriptions = await self.parse_subscriptions(tasks)

                    if error_subscriptions:
                        self.error_log(error_subscriptions)
                        await asyncio.sleep(30)
                        tasks = self.make_tasks(error_subscriptions)
                        error_subscriptions = await self.parse_subscriptions(tasks)

                        if error_subscriptions:
                            self.error_log(error_subscriptions)
                            await asyncio.sleep(90)
                            error_subscriptions = await self.parse_subscriptions(tasks)

                            log.error(
                                "\n".join(
                                    [
                                        f"Не спарсил {subscription.service_name} {subscription.product.name}"
                                        for subscription in error_subscriptions
                                    ]
                                )
                            )
                finally:
                    self.display.stop()
                log.info(f"========end parsing errors count={len(error_subscriptions)}==========")

            await asyncio.sleep(10)

    async def parse_subscriptions(self, tasks) -> list:
        error_subscriptions = []
        for task in asyncio.as_completed(tasks):
            product_data = await task

            if not product_data.name or not product_data.price:
                error_subscriptions.append(product_data.subscription)
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

        return error_subscriptions

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

    def error_log(self, error_subscriptions: list[Subscription]):
        log.info(
            f"===========errors count={len(error_subscriptions)} "
            f"{OZON}={len([item for item in error_subscriptions if item.service_name == OZON])} "
            f"{WILDBERRIES}={len([item for item in error_subscriptions if item.service_name == WILDBERRIES])} "
            f"{YANDEX_MARKET}={len([item for item in error_subscriptions if item.service_name == YANDEX_MARKET])} "
            f"==========="
        )
