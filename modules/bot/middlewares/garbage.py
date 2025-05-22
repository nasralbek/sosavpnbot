import logging

from typing import Any, Awaitable, Callable

from modules.bot.utils.navigation import NavMain

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

logger = logging.getLogger(__name__)


class GarbageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        logger.debug("Garbage Middleware initialized.")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Update) and event.message:
            user_id = event.message.from_user.id

            if user_id == event.bot.id:
                logger.debug(f"Message from bot {event.bot.id} skipped.")
            elif (
                event.message.text
                # and not event.message.text.endswith(NavMain.MAIN)
                # or event.message.forward_from
            ):
                try:
                    await event.message.delete()
                    logger.debug(f"Message {event.message.text} from user {user_id} deleted.")
                except Exception as exception:
                    logger.error(f"Failed to delete message from user {user_id}: {exception}")

        return await handler(event, data)