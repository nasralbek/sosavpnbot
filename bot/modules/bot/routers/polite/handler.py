import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from modules.bot.models.services_container import ServicesContainer
from modules.bot.utils.navigation import NavPolite
from modules.database.models.user import User
from modules.utils.constants import MAIN_MESSAGE_ID_KEY
from tools.image_container import ImageContainer

from .keyboard import polite_keyboard

logger = logging.getLogger(__name__)
router = Router()

def prepare_text():
    return _("polite:message:main")

@router.callback_query(F.data == NavPolite.MAIN)
async def polite_handler(callback: CallbackQuery,
                  user : User,
                  state : FSMContext,
                  services : ServicesContainer,
                  session : AsyncSession,
                  config: Config,
                    images : ImageContainer):
    
    text = prepare_text()
    markup = polite_keyboard(config)


    result =  await callback.message.edit_media(media = InputMediaPhoto(media    = images.service,
                                                                       caption  = text),
                                                text=text,
                                               reply_markup=markup)
 
    return result
