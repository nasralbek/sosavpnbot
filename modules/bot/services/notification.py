from datetime import timedelta
import logging
import asyncio

from aiogram.filters import callback_data
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.methods import edit_message_caption
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic_core.core_schema import str_schema

from config import Config
from aiogram import Bot

from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
    InputMediaUnion,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    chat_id_union,
    message_id,
)

#from modules.bot.routers.misc.keyboard import close_notification_keyboard
from modules.database.models.transaction import Transaction
from modules.database.models.user import User
from modules.utils.constants import MAIN_MESSAGE_ID_KEY, PREVIOUS_MESSAGE_ID_KEY, REACTS_IDS
from modules.bot.utils.navigation import NavMain,NavNotify, NavProfile, NavPurshare
from tools.image_container import ImageContainer

logger = logging.getLogger(__name__)

ReplyMarkupType = (
    InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None
)
def close_notification_keyboard():
    builder = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text = "close", callback_data = NavNotify.CLOSE)
    builder.row(button)
    return builder.as_markup()

def back_to_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text = _("main_menu:button:main"), callback_data = NavMain.MAIN)
    builder.row(button)
    return builder.as_markup()

def expire_event_keyboard():
    builder = InlineKeyboardBuilder()
    
    purchare = InlineKeyboardButton(text = _("main_menu:button:purshare"),
                                    callback_data = NavPurshare.MAIN)
    main_menu = InlineKeyboardButton(text = _("main_menu:button:main"),
                                     callback_data = NavMain.MAIN)
    builder.row(purchare)
    builder.row(main_menu)
    return builder.as_markup()

def pizdaliz_keyboard():
    builder = InlineKeyboardBuilder()
    
    connect = InlineKeyboardButton(text = _("main_menu:button:profile"),
                                   callback_data=NavProfile.MAIN)
    main_menu = InlineKeyboardButton(text = _("main_menu:button:main"),
                                     callback_data = NavMain.MAIN)
    builder.row(connect)
    builder.row(main_menu)
    return builder.as_markup()


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
                 storage : RedisStorage,
                 images : ImageContainer):
        self.config = config
        self.bot = bot
        self.storage = storage
        self.images = images
        logger.info("Notification Service initialized")
    

    @staticmethod 
    async def _notify_admins(
        text:               str,
        config: Config,
        *,
        duration:           int = 0,
        message:            Message     | None  = None,
        reply_markup:       ReplyMarkupType     = None,
        document:           InputFile   | None  = None,
        bot:                Bot         | None  = None,
        message_effect_id:  str         | None  = None
    ):

        logger.info(f"text : {text} for admins notify")
        for chat_id in config.bot.ADMINS:
            logger.info(f"admin {chat_id} notified")
            await NotificationService._notify(
                                text                = text,
                                duration            = duration,
                                chat_id             = chat_id,
                                reply_markup        = reply_markup,
                                document            = document,
                                bot                 = bot,
                                message_effect_id   = message_effect_id
            )

    @staticmethod
    async def _notify(
        text:               str,
        duration:           int,
        *,
        message:            Message     | None  = None,
        chat_id:            int         | None  = None,
        reply_markup:       ReplyMarkupType     = None,
        document:           InputFile   | None  = None,
        photo:              FSInputFile | None  = None,
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

        if photo:
            send_method = bot.send_photo
            args = {"photo": photo, "caption": text}
        elif document:
            send_method = bot.send_document
            args = {"document" : document, "caption": text}
        else:
            send_method = bot.send_message
            args = {"text" : text}

        if message_effect_id: 
            args["message_effect_id"] = message_effect_id
        
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
    async def _notify_replace_previous_message(
        text:               str,
        storage: RedisStorage,
        *,
        duration:           int                 = 0,
        message:            Message     | None  = None,
        chat_id:            int         | None  = None,
        reply_markup:       ReplyMarkupType     = None,
        document:           InputFile   | None  = None,
        photo:              FSInputFile | None  = None,
        bot:                Bot         | None  = None,
        message_effect_id:  str         | None  = None
    ):        
        if message and not bot:
            bot = message.bot

        chat_id = message.chat.id if message else chat_id

        state: FSMContext = FSMContext(
            storage = storage,
            key = StorageKey(bot_id  = bot.id,
                             chat_id = chat_id,
                             user_id = chat_id)
        )
        previous_msg_id =await state.get_value(MAIN_MESSAGE_ID_KEY)
        if not reply_markup:
            reply_markup = back_to_main_menu_keyboard()
        res = await NotificationService._notify(
            text = text,
            duration = duration,
            message = message,
            chat_id = chat_id,
            reply_markup=reply_markup,
            document = document,
            bot = bot,
            photo = photo,
            message_effect_id=message_effect_id
        )
        if isinstance(res,Message):
            await state.update_data({MAIN_MESSAGE_ID_KEY : res.message_id})
            logger.info(f"{previous_msg_id}")
            await bot.delete_message(chat_id = chat_id, message_id=previous_msg_id)


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
            logger.error(e)
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



    async def notify_admins_just_text(self,text : str):
        
        await NotificationService._notify_admins(text = text,config=self.config,bot = self.bot)


    async def notify_expires_soon(self,
                                  user_tg_id: int | str,
                                  days_before: int) -> bool:
        text = _("expire:message:will_expire").format(days = days_before)
        return await self.notify_expire_event(user_tg_id,text)
        
    async def notify_expired(self,
                             user_tg_id: int | str) -> bool:

        text = _("expire:message:expired")
        return await self.notify_expire_event(user_tg_id,text=text)

    async def notify_expired_day_ago(self,user_tg_id) -> bool:
        #todo add days increasing
        #todo add database mark
        #todo check database mark
        text = _("expire:message:expired_day_ago")
        return await self.notify_expire_event(user_tg_id,text=text)

    async def notify_expire_event(self,
                                  user_tg_id: int | str,
                                  text : str) -> bool:
        try:
            if isinstance(user_tg_id,str):
                user_tg_id = int(user_tg_id)
            bot = self.bot
            reply_markup = expire_event_keyboard()
            await NotificationService._notify_replace_previous_message(
                text     = text,
                duration = 0,
                bot      = bot,
                chat_id  = user_tg_id,
                storage  = self.storage,
                reply_markup = reply_markup,
                photo = self.images.notify,
                message_effect_id=REACTS_IDS.poop.value
                                                                       )
            return True
        except Exception as e:
            logger.error(f"{e}")
            return False
        

    async def notify_payment_succeeded(self,
                                        user : User,
                                       transaction : Transaction
                                       ):
        logger.info(f"sending purschare notify to user : {user.tg_id}")
        text = _("purchare:message:success").format(days = transaction.days)
        bot = self.bot
        chat_id = user.tg_id
        result = await NotificationService._notify_replace_previous_message(
            text        = text,
            chat_id     = chat_id,
            bot         = bot,
            storage = self.storage,
            photo = self.images.purschare_success,
            message_effect_id= REACTS_IDS.gratz.value
        )
        return result
        
    async def notify_referral_purschared(self,
                                            User: User,
                                            timedelta: timedelta):
        text = _("notify:message:payment_from_ref").format(days = timedelta.days) 
        result = await NotificationService._notify_replace_previous_message(
            text = text,
            chat_id = User.tg_id,
            bot = self.bot,
            storage = self.storage,
            photo = self.images.purschare_success,
            message_effect_id=REACTS_IDS.gratz.value
        )
        return result
    

    async def notify_pizdaliz(self,user):
        
        text = _("notify:message:pizdaliz").format(days = self.config.shop.PIZDALIZ_REWARD_PERIOD) 
        reply_markup = pizdaliz_keyboard()
        await NotificationService._notify_replace_previous_message(text         = text,
                                                                    chat_id     = user.tg_id,
                                                                    bot         = self.bot,
                                                                    storage     = self.storage,
                                                                   photo = self.images.purschare_success,
                                                                   reply_markup = reply_markup)

    async def notify_referred(self,user : User):
        text = "referred"
        await NotificationService._notify_replace_previous_message(text         = text,
                                                                    chat_id     = user.tg_id,
                                                                    bot         =self.bot,
                                                                    storage     = self.storage
        )

    async def notify_referrer(self,user: User):
        text = _("notify:message:registered_by_ref").format(days = self.config.shop.REFERRER_REWARD_PERIOD)
        await NotificationService._notify_replace_previous_message(text         = text,
                                                                    chat_id     = user.tg_id,
                                                                    bot         = self.bot,
                                                                    storage     = self.storage,
                                                                   photo = self.images.purschare_success,
                                                                   message_effect_id=REACTS_IDS.fire.value
        )

    async def notify_user_first_connected(self,tg_id: int):
        text = _("notify:message:first_connected")
        await NotificationService._notify_replace_previous_message(text     = text,
                                                                   chat_id  = tg_id,
                                                                   bot      = self.bot,
                                                                   storage  = self.storage,
                                                                   photo    = self.images.notify,
                                                                   message_effect_id=REACTS_IDS.gratz.value)


















