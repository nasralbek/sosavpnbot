import logging

from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware,Bot
from aiogram.types import TelegramObject, Update, Message

from pydantic import BaseModel

from modules.utils.constants import PREVIOUS_MESSAGE_ID_KEY
from modules.bot.utils.navigation import NavMain

logger = logging.getLogger(__name__)


class RemoveMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        logger.debug("Log Middleware initialized.")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]) -> Any:
        response =  await handler(event,data)

        state = data['state']
        bot : Bot = data['bot']
        previous_message_id = await state.get_value(PREVIOUS_MESSAGE_ID_KEY)
        try:
            await bot.delete_message(response.chat.id,previous_message_id)
        except:
            pass
        await state.update_data({PREVIOUS_MESSAGE_ID_KEY: response.message_id})

        return response 
        if not isinstance(response, Message): return response
        bot : Bot = data['bot']
        state = data['state']
        previous_message_id = await state.get_value(PREVIOUS_MESSAGE_ID_KEY)
        new_message_id      = response.message_id
        chat_id             = event.event.chat.id

        
        await state.update_data({PREVIOUS_MESSAGE_ID_KEY: new_message_id})
        try:
            logger.debug("deleteing previous message")
            await bot.delete_message(chat_id=chat_id,message_id=previous_message_id)
        except Exception as e:
            logger.warning(e)


        return response
