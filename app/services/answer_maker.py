from typing import (
    Sequence,
)

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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
            created_at = subscription.price_history[-1].created_at if subscription.price_history else subscription.product.created_at
            result.append(f"{subscription.service_name}\n{created_at.strftime('%Y-%m-%d %H:%M')}\n{subscription.product.name}\n{price}₽")

        return {
            "text": "\n\n".join(result)
        }

    def list_subscriptions_keyboard(self, subscriptions: Sequence[Subscription], prefix: str, text: str) -> dict:
        if not subscriptions:
            return self.no_subscriptions()

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"{subscription.service_name} {subscription.product.name}",
                        callback_data=f"{prefix}{subscription.id}")
                ]
                for subscription in subscriptions
            ]
        )

        return {
            "text": text,
            "reply_markup": keyboard,
        }


    def success_subscribe(self, subscription: Subscription) -> str:
        return (
            f"Подписался на\n\n{subscription.service_name}\n\n"
            f"{subscription.product.name}\n\nЦена {subscription.product.price}₽"
        )

    def error_subscribe(self) -> str:
        return "Чет не получилось подписаться, попробуй позже"

    def in_progress(self, name: str) -> str:
        return f"Ага {name}, попытаюсь подписаться на это, это может занять какое то время."

    def history_message(self, subscription: Subscription) -> str:
        result_lines = []
        previous_price = None

        for item in subscription.price_history:
            price = item.price
            date_str = item.created_at.strftime("%Y-%m-%d %H:%M:%S")

            if price != previous_price:
                result_lines.append(f"{date_str} — 💰 {price} руб.")
                previous_price = price

        prices = "\n".join(result_lines)

        return f"<b>{subscription.product.name}</b>\n{prices}"


answer_maker = AnserMaker()
