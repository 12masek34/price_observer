from datetime import (
    UTC,
    datetime,
)

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
)
from sqlalchemy.orm import (
    relationship,
)

from app.database.models.base import (
    MyBase,
)


class PriceHistory(MyBase):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    subscription = relationship("Subscription", back_populates="price_history")
