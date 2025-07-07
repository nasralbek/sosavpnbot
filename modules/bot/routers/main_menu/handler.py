import logging

from aiogram import F, Router,Bot
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from modules.bot.models import ServicesContainer
from modules.database.models import User
from modules.bot.utils.navigation import NavMain
from modules.utils.constants import (PREVIOUS_CALLBACK_KEY,
                                        MAIN_MESSAGE_ID_KEY,
                                        PREVIOUS_MESSAGE_ID_KEY,
                                        HELLO_EMOJI_ID_KEY
)
from modules.bot.filters import ReplyButtonFilter
from modules.bot.filters import IsAdmin

from config import Config
from .keyboard import main_menu_keyboard

logger = logging.getLogger(__name__)
router = Router(name=__name__)



async def redirect_to_main_menu(
    bot:Bot,
    user: User,
    services: ServicesContainer,
    config: Config,
    storage : RedisStorage | None = None,
    state: FSMContext | None = None,
) -> Message | None:
    logger.info(f"user {user.tg_id} redirected to main menu")
    if not state:
        state: FSMContext = FSMContext(
            storage = storage,
            key = StorageKey(bot_id = bot.id,
                             chat_id = user.tg_id,
                             user_id=user.tg_id)
        )
    main_message_id = await state.get_value(MAIN_MESSAGE_ID_KEY)
    is_admin = await IsAdmin()(user_id = user.tg_id)

    try:
        chat_id = user.tg_id
        text = "main_menu"
        reply_markup = main_menu_keyboard(is_admin,
                                          is_refferal_avaible=config.shop.REFERRER_REWARD_ENABLED)

        result = await bot.send_message(chat_id=chat_id,
                               text = text,
                               reply_markup=reply_markup)
        await state.update_data({MAIN_MESSAGE_ID_KEY: result.message_id})
        if main_message_id:
            await bot.delete_message(chat_id = chat_id, message_id = main_message_id)
        
        return result
    except Exception as e:
        logger.error(f"Error redirecting to main menu: {e}")
        return None

def create_refferral(session: AsyncSession,
                     user: User,
                     inviter_id : int) -> None:
    invited_id = user.tg_id
    if inviter_id == user.tg_id:
        return
    logger.info(f"creating reffered {inviter_id} for refferer {inviter_id}") 

@router.message(Command(NavMain.MAIN))
async def command_main_menu(
                    message     : Message,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession,
                    command     : CommandObject,
                    is_new_user : bool):
    if is_new_user and command.args:
        if command.args.isdigit():
            inviter_id = int(command.args)
            create_refferral(session,user,inviter_id)


    emoij_id = await  state.get_value(HELLO_EMOJI_ID_KEY)

    if emoij_id:
        try:
            await message.bot.delete_message(chat_id=user.tg_id,message_id = emoij_id) 
        except Exception as e:
            pass

    emoji_message = await message.bot.send_message(chat_id = user.tg_id,text= "👋",message_effect_id="5046589136895476101")
    await state.update_data({HELLO_EMOJI_ID_KEY: emoji_message.message_id})

 
    response = await redirect_to_main_menu(
            bot = message.bot,
            user = user,
            services = services,
            config = config,
            state = state)

    return response

@router.callback_query(F.data==NavMain.MAIN)
async def callback_main_menu(
                    callback    : CallbackQuery,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession):
    
   
    response = await redirect_to_main_menu(
            bot = callback.message.bot,
            user = user,
            services = services,
            config = config,
            state = state)
                                           
    return response


