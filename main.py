#from modules.yookassaAPI.yookassa_handler import Yookassa_handler
import asyncio 
from urllib.parse import urljoin

from aiohttp.web import Application, _run_app
from config import load_config, Config, DEFAULT_BOT_HOST

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from modules import logger
import modules.bot.middlewares as middlewares
import logging



import modules.bot.filters as filters
from modules.database.database import DataBase
import modules.bot.routers as routers
from modules.utils.constants import(TELEGRAM_WEBHOOK)
import modules.bot.utils.commands as commands

async def on_shutdown(db: DataBase, bot: Bot, ) -> None:
    # services: ServicesContainer
    # await services.notification.notify_developer(BOT_STOPPED_TAG)
    # await commands.delete(bot)
    await bot.delete_webhook()
    await bot.session.close()
    await db.close()
    logging.info("Bot stopped.")

async def on_startup(config: Config,bot: Bot, db: DataBase) -> None:
    #   services: ServicesContainer
    webhook_url = urljoin(config.bot.DOMAIN, TELEGRAM_WEBHOOK)

    print(webhook_url)
    if await bot.get_webhook_info() != webhook_url:
        await bot.set_webhook(webhook_url)

    current_webhook = await bot.get_webhook_info()
    logging.info(f"Current webhook URL: {current_webhook.url}")

#     await services.notification.notify_developer(BOT_STARTED_TAG)
    logging.info("Bot started.")
#     tasks.transactions.start_scheduler(db.session)
#     if config.shop.REFERRER_REWARD_ENABLED:
#         tasks.referral.start_scheduler(
#             session_factory=db.session, referral_service=services.referral
#         )



async def main():
    app = Application()
    config = load_config()

    logger.setup_logging(config.logging)

    db = DataBase(config.database)
    await db.initialize()

    storage = RedisStorage.from_url(url=config.redis.url())

    bot = Bot(
        token=config.bot.TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True),
    )

    #services_container = await services.initialize(config=config, session=db.session, bot=bot)
    #await services_container.server_pool.sync_servers()

    
    # Create the dispatcher
    dispatcher = Dispatcher(
        db=db,
        storage=storage,
        config=config,
        bot=bot,
        # services=services_container,
        # gateway_factory=gateway_factory,
    )

    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    middlewares.MaintenanceMiddleware.set_mode(True)

    middlewares.register(dispatcher=dispatcher, session=db.session)

    filters.register(
        developer_id = config.bot.DEV_ID,
        admins_ids   = [] 
    )

    routers.include(app=app, dispatcher=dispatcher)

    await commands.setup(bot)

    webhook_requests_handler = SimpleRequestHandler(dispatcher=dispatcher, bot=bot)
    webhook_requests_handler.register(app, path=TELEGRAM_WEBHOOK)

    setup_application(app, dispatcher, bot=bot)
    await _run_app(app, host=DEFAULT_BOT_HOST, port=config.bot.PORT)

if __name__=="__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
