import asyncio

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.fsm.storage.memory import (
    MemoryStorage,
)

from app.config.settings import (
    log,
    settings,
)
from app.routers import (
    commands,
    subscribe,
)

dp = Dispatcher(storage=MemoryStorage())


async def main():
    bot = Bot(token=settings.bot_token)
    dp.include_router(commands.router)
    dp.include_router(subscribe.router)
    await bot.delete_webhook(drop_pending_updates=True)
    log.info("application running successfully")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
