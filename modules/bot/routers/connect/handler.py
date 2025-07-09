import asyncio
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
import logging

from aiogram import F, Router
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from modules.bot.models import ServicesContainer
from modules.bot.services.vpn import VPNService
from modules.database.models import User 
from modules.bot.utils.navigation import NavProfile, NavMain
from modules.utils.constants import PREVIOUS_CALLBACK_KEY
from modules.bot.filters import ReplyButtonFilter

from .keyboard import connect_keyboard
from config import Config

logger = logging.getLogger(__name__)
router = Router(name=__name__)

async def prepare_message(user: User,vpn_service:VPNService,config: Config) ->str:
    return _("connect:message:main")

@router.callback_query(F.data == NavProfile.MAIN)
async def profile(
    callback: CallbackQuery,
    user: User,
    services: ServicesContainer,
    state: FSMContext,
    config: Config
):
    logger.info(f"User {user.tg_id} opened connect page.")
    await state.update_data({PREVIOUS_CALLBACK_KEY: NavMain.MAIN})
    
    text = await prepare_message(user,services.vpn,config)
    reply_markup = connect_keyboard() 

    result =  await callback.message.edit_text( text = text,                                                                                        reply_markup=reply_markup,)
    return result

