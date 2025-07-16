from datetime import timedelta
import logging

from aiogram import F, Router,Bot
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
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
from tools.image_container import ImageContainer
from .keyboard import main_menu_keyboard

logger = logging.getLogger(__name__)
router = Router(name=__name__)


async def prepare_text( services    : ServicesContainer,
                        user        : User,
                        is_new_user : bool = False,
                        is_invited  : bool = False,) -> str:

    remaining_time = await services.vpn.get_remaining_time(user)
    no_time = timedelta()
    delta_days = timedelta(days = 1)  
    if not remaining_time:
        remaining_time=no_time
    if remaining_time<no_time:
        delta_days = timedelta(days = 0)
        remaining_time = no_time

    remaining_days = (remaining_time+delta_days).days
    balance = f'{remaining_days}'
    text = _("main_menu:message:main").format(id = user.tg_id,
                                              balance = balance)
    if is_new_user:
        text += _("main_menu:message:new_user")
    #if is_invited:
        #text += _("main_menu:message:invited")
    return text

async def redirect_to_main_menu(
    bot             : Bot,
    user            : User,
    services        : ServicesContainer,
    config          : Config,
    images          : ImageContainer ,
    storage         : RedisStorage  | None  = None,
    state           : FSMContext    | None  = None,
    is_new_user     : bool                  = False,
    is_invited      : bool                  = False,
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

    text = await prepare_text(is_new_user = is_new_user,
                        is_invited=is_invited,
                        user = user,
                        services = services) 
    try:
        chat_id = user.tg_id
        reply_markup = main_menu_keyboard(config,
                                            is_admin,
                                          is_refferal_avaible=config.shop.REFERRER_REWARD_ENABLED)

        result = await bot.send_photo(chat_id=chat_id,
                               caption = text,
                                photo = images.main_menu,
                               reply_markup=reply_markup)
        logger.info("editing media")
        await state.update_data({MAIN_MESSAGE_ID_KEY: result.message_id})
        if main_message_id:
            await bot.delete_message(chat_id = chat_id, message_id = main_message_id)
        
        return result
    except Exception as e:
        logger.error(f"Error redirecting to main menu: {e}")
        return None

async def create_refferral( session     : AsyncSession,
                            services    : ServicesContainer,
                            config      : Config,
                            user        : User,
                            inviter_id  : int) -> bool:
    logger.info(f"creating reffered {inviter_id} for refferer {inviter_id}") 
    invited_id = user.tg_id
    if inviter_id == user.tg_id:
        logger.info("createing referral canceled invited_id = user_id")
        return False
    try:
        await User.update(session = session,tg_id=user.tg_id,invited_by = inviter_id)
        ref = await User.get(session = session, tg_id=inviter_id)
        await User.update(session = session,tg_id=inviter_id,referrals=ref.referrals+1 )

        if config.shop.REFERRER_REWARD_ENABLED:
            await services.vpn.add_days(ref, timedelta(days = config.shop.REFERRER_REWARD_PERIOD))
            await services.notification.notify_referrer(ref)
        if config.shop.REFERRED_TRIAL_ENABLED:
            await services.vpn.add_days(user,timedelta(days = config.shop.REFERRED_TRIAL_PERIOD))
        
        return True
    except Exception as e:
        logger.exception(f"exception {e}")
        return False





@router.message(Command(NavMain.MAIN))
async def command_main_menu(
                    message     : Message,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession,
                    command     : CommandObject,
                    is_new_user : bool,
                    images : ImageContainer):
    is_invited = False
    if is_new_user and command.args:
        if command.args.isdigit():
            inviter_id = int(command.args)
            await create_refferral(session      = session,
                                    user        = user,
                                    services    = services,
                                    config      = config,
                                    inviter_id  = inviter_id)
            is_invited = True

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
            state = state,
            is_new_user = is_new_user,
            is_invited = is_invited,
            images = images)

    return response

@router.callback_query(F.data==NavMain.MAIN)
async def callback_main_menu(
                    callback    : CallbackQuery,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession,
                    images      : ImageContainer):
    
   
    response = await redirect_to_main_menu(
            bot = callback.message.bot,
            user = user,
            services = services,
            config = config,
            state = state,
            images = images)
                                           
    return response


