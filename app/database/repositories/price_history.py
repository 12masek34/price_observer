from decimal import (
    Decimal,
)

from sqlalchemy.exc import (
    IntegrityError,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.config.settings import (
    log,
)
from app.database.models.price_history import (
    PriceHistory,
)
from app.database.models.subscription import (
    Subscription,
)
from app.database.repositories.base import (
    BaseRepository,
)


class PriceHistoryRepository(BaseRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, subscription: Subscription, price: str) -> PriceHistory | None:
        try:
            price_history = PriceHistory(
                subscription=subscription,
                price=Decimal(price),
            )
        except Exception:
            log.exception(f"{price=}")
            return

        self.session.add(price_history)
        try:
            await self.session.commit()
        except IntegrityError as e:
            log.error(e)
            return
        await self.session.refresh(price_history)

        return price_history
