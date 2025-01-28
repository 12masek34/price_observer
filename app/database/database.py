from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import (
    declarative_base,
)

from app.config.settings import (
    settings,
)


engine = create_async_engine(settings.database_url(), echo=True)
session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
   async with session() as db_session:
        try:
            yield db_session
        finally:
            await db_session.close()
