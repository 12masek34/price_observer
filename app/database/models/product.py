from datetime import (
    UTC,
    datetime,
)

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import (
    relationship,
)

from app.database.models.base import (
    MyBase,
)


class Product(MyBase):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    subscriptions = relationship("Subscription", back_populates="product")
