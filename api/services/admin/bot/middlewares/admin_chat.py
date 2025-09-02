



import logging
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InaccessibleMessage, Message, TelegramObject, callback_query, chat

def extract_chat_id(event: TelegramObject) -> int:
    if isinstance(event, Message):
        return  event.chat.id

    elif isinstance(event, CallbackQuery):
        if event.message:
            return event.message.chat.id
    return -1

def extract_thread_id(event: TelegramObject) -> int:
    if isinstance(event, Message):
        return  event.message_thread_id if event.message_thread_id else -1

    elif isinstance(event, CallbackQuery):
        if event.message:
            if not isinstance(event.message, InaccessibleMessage):
                if isinstance(event.message.message_thread_id, int):
                    return event.message.message_thread_id
    return -1

logger = logging.getLogger('uvicorn.error')
class AdminChatMiddleware(BaseMiddleware):
    def __init__(self, admin_chat_id: int,prefered_thread_id: int):
        self.admin_chat_id = admin_chat_id
        self.prefered_thread_id = prefered_thread_id
        super().__init__()

    async def __call__(self, handler, event, data: dict):
        chat_id = extract_chat_id(event)
        thread_id = extract_thread_id(event)

        if chat_id != self.admin_chat_id:
            logger.info("unauthorized chat id")
            return

        if thread_id != self.prefered_thread_id:
            logger.info("unauthorized thread id")
            return

        return await handler(event, data) 
