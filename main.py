import asyncio
import multiprocessing

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
    wildberries,
)
from app.services.price_checker import (
    PriceChecker,
)


dp = Dispatcher(storage=MemoryStorage())


def run_price_checker() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = Bot(token=settings.bot_token)
    price_checker = PriceChecker(bot, session)

    loop.run_until_complete(price_checker.check_by_delay())


async def main() -> None:
    bot = Bot(token=settings.bot_token)
    dp.include_router(commands.router)
    dp.include_router(ozon.router)
    dp.include_router(subscribe.router)
    dp.include_router(wildberries.router)
    dp.update.middleware(DatabaseMiddleware(session=session))
    await bot.delete_webhook(drop_pending_updates=True)
    log.info("application running successfully")
    process = multiprocessing.Process(target=run_price_checker, daemon=True)
    process.start()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
