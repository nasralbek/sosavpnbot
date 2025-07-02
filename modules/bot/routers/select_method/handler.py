
import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from modules.bot.callbacks import SelectMethodCallback
from modules.bot.models.services_container import ServicesContainer
from modules.bot.routers.select_method.keyboard import confirm_keyboard
from modules.bot.utils.navigation import NavPurshare
from modules.database.models.user import User
from modules.utils.constants import PREVIOUS_CALLBACK_KEY, SELECTED_DAYS_KEY, SELECTED_METHOD_KEY, SELECTED_PRICE_KEY


logger = logging.getLogger(__name__)
router = Router(name=__name__)

async def prepare_message(days,price,method) ->str:
    return f"you want to buy {days} days by {price}rub with {method}"

@router.callback_query(SelectMethodCallback.filter())
async def confirm_purshare(   callback    : CallbackQuery,
                        callback_data : SelectMethodCallback,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession):
    logger.info(f"User {user.tg_id} opened invite page.")

    method = callback_data.method_key

    await state.update_data({SELECTED_METHOD_KEY: method})
    await state.update_data({PREVIOUS_CALLBACK_KEY: NavPurshare.MAIN})

    days  = await state.get_value(SELECTED_DAYS_KEY)
    price = await state.get_value(SELECTED_PRICE_KEY)

    text = await prepare_message(days,price,method)
    markup = confirm_keyboard()
    result =  await callback.message.edit_text(text=text,
                                               reply_markup=markup)
    return result

