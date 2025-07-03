
import logging
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from modules.bot.models.services_container import ServicesContainer
from modules.database.models.user import User

logger = logging.getLogger(__name__)

class RemnawaveRegistrateMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        logger.debug("Register remnawave middleware initialized.")

    async def __call__(self,
                    handler     : Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                    event       : TelegramObject,
                    data        : dict[str, Any]):
        is_new_user : bool = data.get("is_new_user",False)
        services: ServicesContainer = data["services"]
        session: AsyncSession = data['session']
        user : User = data['user']

        if is_new_user or not await services.vpn.is_client_exists(user):
            logger.info(f"user: {user.tg_id} not registered: Registrating")
            resp = await services.vpn.register_user(user)
            await user.update(session,tg_id = user.tg_id,uuid = resp.uuid )

        logger.debug("db session going to handler")
        return await handler(event, data)

