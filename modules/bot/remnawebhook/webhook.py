
import json
import logging
from aiogram import Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp.web import Application, Request, Response
from remnawave_api import RemnawaveSDK
from sqlalchemy.ext.asyncio import async_sessionmaker
from config import Config
from modules.bot.models.services_container import ServicesContainer
from modules.database.models.user import User
from modules.utils.constants import REMNAWAVE_WEBHOOK

logger = logging.getLogger(__name__)

class RemnaWebhook():
    def __init__(
        self,
        app : Application,
        services : ServicesContainer,
        storage : RedisStorage,
        bot: Bot,
        config: Config,
        r_sdk: RemnawaveSDK,
        session : async_sessionmaker
    ):
        self.app        = app
        self.services   = services
        self.storage    = storage
        self.bot        = bot
        self.config     = config
        self.session    = session
        self.r_sdk      = r_sdk
        

        logger.info("remnawave webhook initialized")

    def register_webhook(self):
        self.app.router.add_post(REMNAWAVE_WEBHOOK,self.webhook_handler)
        logger.info(f"remnawave webhook registered at : {REMNAWAVE_WEBHOOK}")

    async def on_service_event(self,event) -> Response:
        text = json.dumps(event, separators=(',', ':'),indent=4)
        await self.services.notification.notify_admins_just_text(text)
        return Response(status = 200)

    async def on_user_first_connected(self,tg_id) -> bool:
        async with self.session() as session:
            try:
                await User.update(session,int(tg_id), firsttime_used = True)
                await self.services.notification.notify_user_first_connected(tg_id)
                return True
            except Exception as e:
                logger.error(f"failed to set mark firsttime_used to user: {tg_id} {e}")
                return False

    async def on_user_event(self,event) -> Response:
        text = json.dumps(event, separators=(',', ':'),indent=4)
        logger.info(event["event"])
        try:
            event_name = event["event"]
            tg_id = event["data"]["telegramId"]
            match event_name:
                case "user.expires_in_48_hours":
                    res = await self.services.notification.notify_expires_soon(tg_id, 2)
                case "user.expires_in_24_hours":
                    res = await self.services.notification.notify_expires_soon(tg_id, 1)
                case "user.expired":
                    res = await self.services.notification.notify_expired(tg_id)
                case "user.first_connected":
                    res = await self.on_user_first_connected(tg_id)            
                case _:
                    return Response(status = 500)
                #case "user.expired_24_hours_ago":
                #    res = await self.services.notification.notify_expired_day_ago(tg_id)
            if res:
                return Response(status = 200)
            logger.info(f"{event["event"]} not handled ")
            return Response(status = 501)
        except Exception as e:
            logger.exception(f"catched exception {e} ")
            return Response(status = 500)

    async def event_handler(self,event) -> Response:
        event_name : str= event["event"]
        if event_name.startswith("service."):
            return await self.on_service_event(event)
        if event_name.startswith("user"):
            return await self.on_user_event(event)



        logger.info(f"event ({event_name}) from remna webhook not handled")
        return Response(status=501)



    async def webhook_handler(self,request : Request) -> Response:
        try:
            body : dict = await request.json() 
            body_text = await request.text()
            headers = request.headers 
            signature = headers["X-Remnawave-Signature"]
            

            webhook_secret = self.config.remnawave.WEBHOOK_SECRET



            if not self.r_sdk.webhook_utility.validate_webhook( body_text,
                                                                signature,
                                                                webhook_secret):
                logger.info(f"webhook not passed {body['event']}")
                return Response(status = 403)
                
            else:
                logger.info(f"webhook passed {body['event']}")
        except Exception as e:
            logger.error(e)
            return Response(status = 400)
        
        logger.info(f"going to check {body["event"]}")
        return await self.event_handler(body)
        
