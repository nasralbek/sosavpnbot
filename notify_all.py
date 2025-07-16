




#from modules.yookassaAPI.yookassa_handler import Yookassa_handler
import logging
import asyncio 
from urllib.parse import urljoin

from aiohttp.web import Application, _run_app
from remnawave_api import RemnawaveSDK
from sqlalchemy import text
from config import DatabaseConfig, load_config, Config, DEFAULT_BOT_HOST,DEFAULT_LOCALES_DIR

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
#from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n

from modules.bot.payment_gateways.gateway_factory import GatewayFactory
from modules.bot.remnawebhook.webhook import RemnaWebhook
from modules.logger import logger,get_start_log_message

import modules.bot.middlewares as middlewares
from modules.database.database import DataBase
from modules.utils.constants import(
                            TELEGRAM_WEBHOOK,
                            DEFAULT_LANGUAGE,
                            I18N_DOMAIN
                            )
from modules.bot import services,routers,filters
from modules.bot.utils import commands
from modules.bot.models import ServicesContainer
from tools.image_container import ImageContainer, load_images

from modules.database.models.user import User



config = load_config()



#COPY FROM MIGRATE
new_db_config = DatabaseConfig(
    HOST = "",
    PORT = 321,
    NAME = "",
    USERNAME = "",
    PASSWORD=  ""
)



async def get_all_users(db : DataBase):
    async with db.session() as s:
        res = await s.execute(text("select * from users"))
        all = res.fetchall()
    return all



async def main():

    db = DataBase(new_db_config)
 

    storage = RedisStorage.from_url(url=config.redis.url())

    bot = Bot(
        token=config.bot.TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True),
    )

    i18n = I18n(path=DEFAULT_LOCALES_DIR, default_locale=DEFAULT_LANGUAGE, domain=I18N_DOMAIN)
    I18n.set_current(i18n)


    r_sdk = RemnawaveSDK(   base_url  = config.remnawave.PANEL_URL,
                            token     = config.remnawave.TOKEN)

    images : ImageContainer = load_images()
    services_container = await services.initialize(config   = config, 
                                                   session  = db.session, 
                                                   bot      = bot,
                                                   storage  = storage,
                                                   r_sdk = r_sdk,
     
                                                   images = images)
    












    async with db.session() as s:

        #UNCOMMENT WHEN YOU READY
        #users = await User.get_all(session = db.session())

        users = [await User.get(session = db.session(),tg_id = 399365366)] #remove after tests


    text = "dsadsadsa"


    for user in users:
        await services_container.notification._notify_replace_previous_message(
            storage = storage,
            chat_id = user.tg_id,
            text = text,
            bot = bot,
            duration=0,
        )
        


if __name__=="__main__":
    asyncio.run(main())
