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
from app.database.database import (
    session,
)
from app.middlewares.database import (
    DatabaseMiddleware,
)
from app.routers import (
    commands,
    ozon,
    subscribe,
)
from app.services.price_checker import (
    PriceChecker,
)


dp = Dispatcher(storage=MemoryStorage())

async def main():
    bot = Bot(token=settings.bot_token)
    price_checker = PriceChecker(bot, session)
    dp.include_router(commands.router)
    dp.include_router(ozon.router)
    dp.include_router(subscribe.router)
    dp.update.middleware(DatabaseMiddleware(session=session))
    await bot.delete_webhook(drop_pending_updates=True)
    log.info("application running successfully")
    asyncio.create_task(price_checker.check_by_delay())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
