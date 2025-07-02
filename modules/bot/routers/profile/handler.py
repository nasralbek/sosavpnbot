import asyncio
import logging

from aiogram import F, Router
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from modules.bot.services import ServicesContainer
from modules.database.models import User
from modules.bot.utils.navigation import NavProfile, NavMain
from modules.utils.constants import PREVIOUS_CALLBACK_KEY
from modules.bot.filters import ReplyButtonFilter

from .keyboard import connect_keyboard
from config import Config

logger = logging.getLogger(__name__)
router = Router(name=__name__)

async def prepare_message(user: User, client_data,config: Config) ->str:
    print(config)
    vpn_name        = config.bot.BOT_VPN_NAME
    day_price       = config.shop.DAY_PRICE
    status          = "|тут будет статус|"
    balance         = "|тут будет баланс|"
    remaining_days  = "|тут будут отс. дни|" 

    return _("profile:message:main").format(
        vpn_name        = vpn_name,
        status          = status,
        day_price       = day_price,
        balance         = balance,
        remaining_days  = remaining_days 
    )

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
    client_data = None

    text = await prepare_message(user,client_data,config)
    reply_markup = connect_keyboard() 

    result =  await callback.message.edit_text( text = text,
                                                reply_markup=reply_markup,)
    return result

