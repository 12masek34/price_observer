from aiogram import (
    types,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.models.subscription import (
    Subscription,
)
from app.parsers.ozon import (
    OzonParser,
)
from app.services.base import (
    BaseSubscriberService,
)


class SubscriberService(BaseSubscriberService):

    def __init__(self, message: types.Message, session: AsyncSession) -> None:
        super().__init__(message, session)
        self.parser = OzonParser(self.get_url())


    async def subscribe(self) -> Subscription:
        product_data = await self.parser.parse()
        product = await self.product_repository.create(product_data.name, product_data.price)
        subscription = await self.subscribe_repository.create(
            self.get_user_id(),
            self.get_chat_id(),
            product.id,
            self.get_user_name(),
            self.get_url(),
        )

        return subscription
