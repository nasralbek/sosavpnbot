


import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from modules.bot.callbacks import HowToCallback, platformEnum
from modules.bot.models.services_container import ServicesContainer
from modules.database.models.user import User

from .keyboard import how_to_keyboard

logger = logging.getLogger(__name__)
router = Router()

def prepare_text(platform : platformEnum):
    return _(f"how_to:platform:message:{platform.value}") 


@router.callback_query(HowToCallback.filter())
async def handle_how_to(callback: CallbackQuery,
                  callback_data : HowToCallback,
                  user : User,
                  state : FSMContext,
                  services : ServicesContainer,
                  session : AsyncSession,
                  config: Config):
    
    text = prepare_text(callback_data.platform)
    key = await services.vpn.get_short_uuid(user)
    markup = how_to_keyboard(callback_data.platform,key = key,config = config)
    result =  await callback.message.edit_caption(caption=text,
                                               reply_markup=markup)
 
    return result
