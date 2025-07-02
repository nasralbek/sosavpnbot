import logging

from aiogram import F, Router
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession

from modules.bot.models import ServicesContainer
from modules.database.models import User
from modules.bot.utils.navigation import NavMain, NavSupport
from modules.utils.constants import PREVIOUS_CALLBACK_KEY
from modules.bot.filters import ReplyButtonFilter
from config import Config

from .keyboard import invite_keyboard


logger = logging.getLogger(__name__)
router = Router(name=__name__)


async def prepare_message(config) ->str:
    return _("support:message:main").format(vpn_name = config.bot.BOT_VPN_NAME)

@router.callback_query(F.data == NavSupport.MAIN)
async def invite(   callback    : CallbackQuery,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession):
    logger.info(f"User {user.tg_id} opened invite page.")
    await state.update_data({PREVIOUS_CALLBACK_KEY: NavSupport.MAIN})
    text = await prepare_message(config)
    markup = invite_keyboard()
    result =  await callback.message.edit_text(text=text,
                                               reply_markup=markup)
    return result

