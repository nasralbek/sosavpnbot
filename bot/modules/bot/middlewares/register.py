
import asyncio
from datetime import timedelta
import logging
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config import Config
from modules.bot.models.services_container import ServicesContainer
from modules.database.models.user import User

logger = logging.getLogger(__name__)

async def procces_pizdaliz(session_maker : async_sessionmaker,
                           services: ServicesContainer,
                           config : Config,
                           tg_id: int):
    if not config.shop.PIZDALIZ_REWARD_ENABLED:
        return
    logger.info("proccess pizdaliz started")
    await asyncio.sleep(60*config.shop.PIZDALIZ_REWARD_DELAY)
    async with session_maker() as s:
        user = await User.get(session = s, tg_id=tg_id) 
        if user.firsttime_used:
            return
        await services.vpn.add_days(user,timedelta(days=config.shop.PIZDALIZ_REWARD_PERIOD))
        await services.notification.notify_pizdaliz(user)

class RemnawaveRegistrateMiddleware(BaseMiddleware):
    def __init__(self,session_maker) -> None:
        logger.debug("Register remnawave middleware initialized.")
        self.session_maker : async_sessionnmaker = session_maker

    async def __call__(self,
                    handler     : Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                    event       : TelegramObject,
                       data        : dict[str, Any]):
        is_new_user : bool = data.get("is_new_user",False)
        services: ServicesContainer = data["services"]
        session: AsyncSession = data['session']
        user : User = data['user']
        config : Config = data['config']

        if is_new_user:
            logger.info(f"user: {user.tg_id} not registered: Registrating")
            resp = await services.vpn.register_user(user)
            await user.update(session,tg_id = user.tg_id,uuid = resp.uuid )
            
            if config.shop.TRIAL_ENABLED:
                await services.vpn.add_days(user,timedelta(days=config.shop.TRIAL_PERIOD))
            asyncio.create_task(procces_pizdaliz(self.session_maker,services,tg_id=user.tg_id,config = config))

        logger.debug("db session going to handler")
        return await handler(event, data)

