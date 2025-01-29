from decimal import Decimal
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.models.price_history import PriceHistory
from app.database.models.subscription import Subscription
from app.database.repositories.base import (
    BaseRepository,
)


class PriceHistoryRepository(BaseRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, subscription: Subscription, price: str) -> PriceHistory:
        price_history = PriceHistory(
            subscription=subscription,
            price=Decimal(price),
        )
        self.session.add(price_history)
        await self.session.commit()
        await self.session.refresh(price_history)

        return price_history
