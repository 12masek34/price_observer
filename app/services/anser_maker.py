from typing import (
    Sequence,
)

from app.database.models.subscription import (
    Subscription,
)


class AnserMaker:

    def list_subscriptions(self, subscriptions: Sequence[Subscription]) -> str:
        if not subscriptions:
            return "Нет подписок"

        return "\n\n".join(
            f"{subscription.service_name}\n{subscription.product.name}\n{subscription.product.price}₽"
            for subscription in subscriptions
        )
