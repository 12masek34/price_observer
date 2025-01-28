from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.models.subscription import (
    Subscription,
)


class SubscriptionRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def create(self, user_id :int, chat_id: int, product_id: int, user_name: str, url: str) -> Subscription:
        subscription = Subscription(
            user_id=user_id,
            chat_id=chat_id,
            product_id=product_id,
            user_name=user_name,
            url=url,
        )
        self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription, ["product"])

        return subscription
