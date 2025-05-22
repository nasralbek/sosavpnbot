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
from config import Config


logger = logging.getLogger(__name__)
router = Router(name=__name__)


async def prepare_message(config) ->str:
    return _("information:message:main").format(vpn_name = config.bot.BOT_VPN_NAME)


async def information(  message : Message,
                        user:User,
                        state:FSMContext,
                        config: Config):
    logger.info(f"User {user.tg_id} opened connect page.")
    await state.update_data({PREVIOUS_CALLBACK_KEY: NavMain.INFORMATION})
    client_data = None

    text = await prepare_message(config)

    result =  await message.answer(text = text,)
    return result

@router.message(ReplyButtonFilter("main_menu:button:information"))
async def information_message(
    message : Message,
    user: User,
    services: ServicesContainer,
    state: FSMContext,
    config: Config
):return await information(message,user,state, config)

@router.callback_query(F.data == NavMain.CONNECT)
async def information_callback(
    callback: CallbackQuery,
    user: User,
    services: ServicesContainer,
    state: FSMContext,
    config: Config,
):return await information(callback.message,user,state,config)
