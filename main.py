import asyncio
import multiprocessing

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.fsm.storage.memory import (
    MemoryStorage,
)
from pyvirtualdisplay.display import (
    Display,
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
    yandex_market,
)
from app.services.price_checker import (
    PriceChecker,
)


dp = Dispatcher(storage=MemoryStorage())


def run_price_checker() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = Bot(token=settings.bot_token)
    price_checker = PriceChecker(bot, session())

    loop.run_until_complete(price_checker.check_by_delay())


async def main() -> None:
    display = Display(visible=False, size=(1920, 1080), backend="xvfb")
    display.start()
    bot = Bot(token=settings.bot_token)
    dp.include_router(commands.router)
    dp.include_router(ozon.router)
    dp.include_router(subscribe.router)
    dp.include_router(wildberries.router)
    dp.include_router(yandex_market.router)
    dp.update.middleware(DatabaseMiddleware(session=session))
    await bot.delete_webhook(drop_pending_updates=True)
    log.info("application running successfully")
    process = multiprocessing.Process(target=run_price_checker, daemon=True)
    process.start()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    display.stop()


if __name__ == "__main__":
    asyncio.run(main())
    # from app.parsers.yandex_market import YandexMarketParser
    # from pyvirtualdisplay.display import (
    #     Display,
    # )
    # Display(visible=False, size=(1920, 1080), backend="xvfb").start()
    # parser = YandexMarketParser(url="https://market.yandex.ru/product--g20-lite/157681807?sku=103778362453&uniqueId=16870397&do-waremd5=YDIpqL-4KT3EAin2T57yUw&cpc=wY_f4C_SsAzmw6mEM_j0AOsFL_S9LMus5jHIiz19luWA2nROeYAFyqK9BR-ZPQA3DDvF2dz_DnY1ij3JH1d08s9rx7QftLDkrCgLZ3SbJudCQtUQKFjgclzU-1TeCbp_xMxX-50dn-RD_nvWXg3iu57MvkCSireJzMObnM0Sgz5F6A8Uru_AKpuLFVABo7x1UYoUAaCcEOZFswLkA9IYufwDSFRtP7GMfRekFUkYdEbd1RceI5Cc5WPYoBF_5aj4iVUQSo9Ggoebr90Wy3TxooiEaZjzH5gnLjaBSLUw6s2wVgg_7fgElYc0oTAhfdxydKmvpGrkkd3REJjOlwbGecaPBZvLv9iPksKQaZmg4KEdZ8dgbOfsfOyBGgFZzyN0")
    # parser.parse()
