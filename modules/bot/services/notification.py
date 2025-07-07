import logging
import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.methods import edit_message_caption
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic_core.core_schema import str_schema

from config import Config
from aiogram import Bot

from aiogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
    InputMediaUnion,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    chat_id_union,
)

#from modules.bot.routers.misc.keyboard import close_notification_keyboard
from modules.database.models.transaction import Transaction
from modules.database.models.user import User
from modules.utils.constants import MAIN_MESSAGE_ID_KEY
from modules.bot.utils.navigation import NavMain

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
    def __init__(self,
                 config: Config,
                 bot : Bot,
                 storage : RedisStorage):
        self.config = config
        self.bot = bot
        self.storage = storage
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
    
    @staticmethod
    async def _notify_message_edit(
        text: str,
        message_id: int,
        chat_id :int,
        bot: Bot,
        *,
        reply_markup: InlineKeyboardMarkup | None = None,
        document: InputMediaUnion | None = None
    )-> Message | bool:
        
        args = {"media": document, "caption": text} if document else {"text": text}
        
        try:
            notification = await bot.edit_message_text(text = text,
                                                       chat_id = chat_id,
                                                       message_id=message_id,
                                                       reply_markup=reply_markup
                                                       )

            if document:
                notification = await bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media = document,reply_markup=reply_markup)
        except Exception as e:
            return False

        return notification 

    @staticmethod
    async def _notify_message_edit_tg_message(
            text: str,
            *,
            message : Message,
            reply_markup: InlineKeyboardMarkup | None = None,
            document: InputMediaUnion | None = None
    ) -> Message | bool:
        message_id = message.message_id
        chat_id    = message.chat.id
        bot        = message.bot
        if not bot:
            logger.error("bot not specified")
            return False 
        return await NotificationService._notify_message_edit(text,message_id = message_id,
                                                       chat_id = chat_id,
                                                       bot=bot)


    async def notify_payment_succeeded(self,
                                        user : User,
                                       transaction : Transaction
                                       ):
        logger.info(f"sending purschare notify to user : {user.tg_id}")
        text = f"thx for purshare,\n\
                your balance been icreased by {transaction.days}"

        bot = self.bot
        state: FSMContext = FSMContext(
            storage = self.storage,
            key = StorageKey(bot_id = bot.id,
                             chat_id = user.tg_id,
                             user_id=user.tg_id)
        )
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text = "main_menu", callback_data=NavMain.MAIN))
        message_id = await state.get_value(MAIN_MESSAGE_ID_KEY) 
        chat_id = user.tg_id
        result = await NotificationService._notify_message_edit(
            text        = text,
            message_id  = message_id,
            chat_id     = chat_id,
            bot         = bot,
            reply_markup=builder.as_markup()
        )
        return result
        



