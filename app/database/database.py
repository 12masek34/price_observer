from typing import (
    AsyncGenerator,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.declarative import (
    declarative_base,
)
from sqlalchemy.orm import (
    sessionmaker,
)

from app.config.settings import (
    settings,
)
engine = create_async_engine(settings.database_url(), echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
