from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    relationship,
)

from app.database.models.base import (
    MyBase,
)


class Subscription(MyBase):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    chat_id = Column(Integer, index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=True)
    user_name = Column(String, nullable=True)
    url = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
    product = relationship(
        "Product",
        back_populates="subscriptions",
        lazy="joined",
    )
    price_history = relationship(
        "PriceHistory",
        back_populates="subscription",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="PriceHistory.id"
    )
