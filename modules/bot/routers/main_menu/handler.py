import logging

from aiogram import F, Router,Bot
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from modules.bot.services import ServicesContainer
from modules.database.models import User
from modules.bot.utils.navigation import NavMain
from modules.utils.constants import PREVIOUS_CALLBACK_KEY,MAIN_MESSAGE_ID_KEY,PREVIOUS_MESSAGE_ID_KEY
from modules.bot.filters import ReplyButtonFilter
from modules.bot.filters import IsAdmin

from config import Config
from .keyboard import main_menu_keyboard

logger = logging.getLogger(__name__)
router = Router(name=__name__)

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
    logger.info(f"user {user.tg_id} opened main menu")
    
    #previsous_message_id     = await state.get_value(PREVIOUS_MESSAGE_ID_KEY)
    #previous_main_message_id = await state.get_value(MAIN_MESSAGE_ID_KEY)
    if is_new_user and command.args:
        if command.args.isdigit():
            inviter_id = int(command.args)
            create_refferral(session,user,inviter_id)

    is_admin = await IsAdmin()(user_id=user.tg_id) 
    text            = "main_menu"
    reply_markup    = main_menu_keyboard(is_admin,config.shop.REFERRER_REWARD_ENABLED)
    response = await message.answer(text,reply_markup=reply_markup)
    return response

@router.callback_query(F.data==NavMain.MAIN)
async def callback_main_menu(
                    callback    : CallbackQuery,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession):
    
    is_admin = await IsAdmin()(user_id=user.tg_id) 
    reply_markup    = main_menu_keyboard(is_admin,config.shop.REFERRER_REWARD_ENABLED)
    text="main_menu"
    response = await callback.message.edit_text(text=text,reply_markup=reply_markup)
    return response

