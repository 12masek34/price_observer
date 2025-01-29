import asyncio
import logging

from app.config.settings import settings
from app.database.database import Base
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

from app.database.models.subscription import Subscription
from app.database.models.product import Product
from app.database.models.price_history import PriceHistory


engine = create_async_engine(settings.database_url())
target_metadata = Base.metadata


async def run_migrations_online():
    """Запуск миграций в асинхронном режиме."""
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    """Конфигурация контекста Alembic и запуск миграций."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    logging.error("offline migration not imptimented")
else:
    asyncio.run(run_migrations_online())