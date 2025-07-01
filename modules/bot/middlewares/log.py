import logging

from typing import Any, Awaitable, Callable, Optional

from modules.bot.utils.navigation import NavMain

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from pydantic import BaseModel

logger = logging.getLogger(__name__)

class EventLogSchema(BaseModel):
    user_id     : int
    username    : str  | None
    firstname   : Optional[str]  | None = None
    lastname    : Optional[str]  | None = None
    callback    : Optional[str]  | None = None 
    text        : Optional[str]  | None = None 



class LogMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        logger.debug("Log Middleware initialized.")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        try:
            logging.info(f"message_id: {event.event.message_id}")
        except:
            pass
        try:
            callback = event.event.data
        except Exception as e:
            #logger.info(event.event)
            callback = None
        try:
            text= event.event.text
        except:
            text = None
        log_data = {
            "user_id"   : event.event.from_user.id,
            "username"  : event.event.from_user.username,
            # "firstname" : event.event.from_user.first_name,
            # "lastname"  : event.event.from_user.last_name,
            "callback"  : callback,
            "text"      : text
        }
        log = EventLogSchema(**log_data)
        logger.info(repr(log))
        #logger.info(event)
        return await handler(event, data)

