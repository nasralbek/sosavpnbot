import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from modules.bot.callbacks import SelectMethodCallback
from modules.bot.models.services_container import ServicesContainer
from .keyboard import purshare_final_keyboard
from modules.bot.utils.navigation import NavPurshare
from modules.database.models.user import User
from modules.utils.constants import PREVIOUS_CALLBACK_KEY, SELECTED_DAYS_KEY, SELECTED_METHOD_KEY, SELECTED_PRICE_KEY


logger = logging.getLogger(__name__)
router = Router(name=__name__)

async def prepare_message(days,price,method,url) ->str:
    return f"you want to buy {days} days by {price}rub with {method},\n\
    your purshare url: {url}"

@router.callback_query(F.data == NavPurshare.CONFIRM)
async def purshare_final(callback    : CallbackQuery,
                        user        : User,
                        state       : FSMContext,
                        services    : ServicesContainer,
                        config      : Config,
                        session     : AsyncSession):
    logger.info(f"User {user.tg_id} opened invite page.")


    days    = await state.get_value(SELECTED_DAYS_KEY)
    price   = await state.get_value(SELECTED_PRICE_KEY)
    method  = await state.get_value(SELECTED_METHOD_KEY)
    
    url = "oplata.url"
    text = await prepare_message(days,price,method,url)
    markup = purshare_final_keyboard()
    result =  await callback.message.edit_text(text=text,
                                               reply_markup=markup)
    return result

