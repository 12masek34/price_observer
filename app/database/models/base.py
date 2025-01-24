from app.database.database import (
    Base,
)


class MyBase(Base):
    __abstract__ = True

    def to_dict(self) -> dict:
        return {field.name: getattr(self, field.name) for field in self.__table__.c}
