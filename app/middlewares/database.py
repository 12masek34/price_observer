
from typing import (
    Any,
    Awaitable,
    Callable,
)

from aiogram import (
    BaseMiddleware,
)
from aiogram.types import (
    TelegramObject,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self.session = session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]) -> Any:

        async with self.session() as session:
            data["session"] = session
            return await handler(event, data)
