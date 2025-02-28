from typing import (
    Sequence,
)

from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.models.subscription import (
    Subscription,
)

from app.database.models.price_history import (
    PriceHistory,
)
from app.database.repositories.base import (
    BaseRepository,
)


class SubscriptionRepository(BaseRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(
        self,
        user_id :int,
        chat_id: int,
        product_id: int,
        user_name: str,
        url: str,
        service_name: str,
    ) -> Subscription:
        subscription = Subscription(
            user_id=user_id,
            chat_id=chat_id,
            product_id=product_id,
            user_name=user_name,
            url=url,
            service_name=service_name,
        )
        self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription, ["product", "price_history"])

        return subscription

    async def get_all_subscrptions(self) -> Sequence[Subscription]:
        stmt = select(Subscription)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_subscrptions_by_user_id(self, user_id: int) -> Sequence[Subscription]:
        stmt = select(Subscription).where(Subscription.user_id == user_id).order_by(Subscription.service_name)
        result = await self.session.scalars(stmt)

        return result.all()

    async def delete_by_id(self, subscription_id: int) -> Subscription:
        subscription = await self.session.get_one(Subscription, subscription_id)

        await self.session.delete(subscription)
        await self.session.commit()

        return subscription

    async def get_subscription_by_id(self, subscription_id: int) -> Subscription:
        return await self.session.get_one(Subscription, subscription_id)
