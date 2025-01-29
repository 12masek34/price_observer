from typing import (
    Sequence,
)

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from app.config.settings import (
    DELETE_SUBSCRIPTION_PREFIX,
)
from app.database.models.subscription import (
    Subscription,
)


class AnserMaker:

    def no_subscriptions(self) -> dict:
        return {"text": "Нет подписок"}

    def list_subscriptions(self, subscriptions: Sequence[Subscription]) -> dict:
        if not subscriptions:
            return self.no_subscriptions()

        result = []
        for subscription in subscriptions:
            price = subscription.price_history[-1].price if subscription.price_history else subscription.product.price
            result.append(f"{subscription.service_name}\n{subscription.product.name}\n{price}₽")

        return {
            "text": "\n\n".join(result)
        }

    def list_subscriptions_keyboard(self, subscriptions: Sequence[Subscription]) -> dict:
        if not subscriptions:
            return self.no_subscriptions()

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"{subscription.service_name} {subscription.product.name}",
                        callback_data=f"{DELETE_SUBSCRIPTION_PREFIX}{subscription.id}")
                ]
                for subscription in subscriptions
            ]
        )

        return {
            "text": "Какую удалить:",
            "reply_markup": keyboard,
        }
