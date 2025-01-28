from decimal import (
    Decimal,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.models.product import (
    Product,
)


class ProductRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def create(self, name: str, price: Decimal) -> Product:
        product = Product(
            name=name,
            price=price,
        )
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)

        return product
