import asyncio
import logging

from aiogram import F, Router
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from modules.bot.services import ServicesContainer
from modules.database.models import User
from modules.bot.utils.navigation import NavMain
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

    return _("connect_vpn:message:main").format(
        vpn_name        = vpn_name,
        status          = status,
        day_price       = day_price,
        balance         = balance,
        remaining_days  = remaining_days 
    )

async def profile(message : Message,
                  user:User,
                  state:FSMContext,
                  config):
    logger.info(f"User {user.tg_id} opened connect page.")
    await state.update_data({PREVIOUS_CALLBACK_KEY: NavMain.MAIN})
    client_data = None

    text = await prepare_message(user,client_data,config)
    reply_markup = connect_keyboard() 

    result =  await message.answer(   text = text,
                            reply_markup=reply_markup,
                        )
    return result


@router.message(ReplyButtonFilter("main_menu:button:connect_vpn"))
async def profile_message(
    message : Message,
    user: User,
    services: ServicesContainer,
    state: FSMContext,
    config: Config
):return await profile(message,user,state,config)

# @router.callback_query(F.data == NavMain.CONNECT)
# async def profile_callback(
#     callback: CallbackQuery,
#     user: User,
#     services: ServicesContainer,
#     state: FSMContext,
# ):return await profile(callback.message,user,state)
