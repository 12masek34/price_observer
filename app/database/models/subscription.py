from sqlalchemy import Column, Integer
from app.database.models.base import MyBase


class Subscription(MyBase):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
