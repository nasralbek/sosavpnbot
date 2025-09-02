





import logging
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

logger = logging.getLogger('uvicorn.error')

def get_id(event: TelegramObject):
    if isinstance(event,Message):
        return event.from_user.id
    if isinstance(event,CallbackQuery):
        return event.from_user.id
    return -1

class AdminMiddleware(BaseMiddleware):
    def __init__(self,admins):
        self.admins = admins
        super().__init__()

    async def __call__(self,
                       handler,
                       event,
                       data:dict):
        if int(get_id(event)) not in self.admins:
            logger.info(f"unauthorized user not in {self.admins}")
            return
        return await handler(event,data)

