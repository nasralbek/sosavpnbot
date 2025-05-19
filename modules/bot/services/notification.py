import logging
import asyncio

from config import Config
from aiogram import Bot

from aiogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardMarkup,
    InputFile,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from modules.bot.routers.misc.keyboard import close_notification_keyboard

logger = logging.getLogger(__name__)

ReplyMarkupType = (
    InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None
)

async def auto_delete(notification,duration):    
    await asyncio.sleep(duration)
    try:
        await notification.delete()
    except Exception as exception:
        logger.error(f"Failed to delete message {notification.message_id}: {exception}")

class NotificationService:
    def __init__(self,config: Config,bot : Bot):
        self.config = config
        self.bot = bot
        logger.info("Notification Service initialized")
    



    @staticmethod
    async def _notify(
        text:               str,
        duration:           int,
        *,
        message:            Message     | None  = None,
        chat_id:            int         | None  = None,
        reply_markup:       ReplyMarkupType     = None,
        document:           InputFile   | None  = None,
        bot:                Bot         | None  = None,
        message_effect_id:  str         | None  = None
    ) -> Message | None:
        if not (message or chat_id):
            logger.error("Failed to send notification: message or chat_id required")
            return None
        
        if message and not bot:
            bot = message.bot

        chat_id = message.chat.id if message else chat_id

        if duration == 0 and reply_markup is None:
            reply_markup = close_notification_keyboard()

        send_method = bot.send_document if document else bot.send_message
        args = {"document": document, "caption": text} if document else {"text": text}
        if message_effect_id: args["message_effect_id"] = message_effect_id
        
        try:
            notification = await send_method(chat_id=chat_id, reply_markup=reply_markup, **args)
            logger.debug(f"Notification sent to {chat_id}")
        except Exception as exception:
            logger.error(f"Failed to send notification: {exception}")
            return None
        
        if duration>0:
            await auto_delete(notification,duration)

        return notification
    
