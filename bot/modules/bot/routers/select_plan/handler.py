
import logging

from aiogram import Router
from modules.bot.models.services_container import ServicesContainer
from modules.bot.routers.select_plan.keyboard import select_method_keyboard
from modules.bot.utils.navigation import NavPurshare
from modules.database.models import User
from modules.utils.constants import PREVIOUS_CALLBACK_KEY,SELECTED_DAYS_KEY, SELECTED_PLAN_KEY,SELECTED_PRICE_KEY
from modules.bot.callbacks import SelectPlanCallback
from config import Config

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)
router = Router(name=__name__)

async def prepare_message(days,price) ->str:
    return _("select_method:message:main").format(days = days,
                                                  price = price)

@router.callback_query(SelectPlanCallback.filter())
async def select_method(   callback    : CallbackQuery,
                        callback_data : SelectPlanCallback,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession):
    logger.info(f"User {user.tg_id} opened invite page.")

    days        = callback_data.days
    price       = callback_data.price
    plan_name   = callback_data.name


    await state.update_data({SELECTED_DAYS_KEY  : days})
    await state.update_data({SELECTED_PRICE_KEY : price})
    await state.update_data({SELECTED_PLAN_KEY  : plan_name })


    await state.update_data({PREVIOUS_CALLBACK_KEY: NavPurshare.MAIN})
    text = await prepare_message(days,price)
    markup = select_method_keyboard(config)
    result =  await callback.message.edit_caption(caption=text,
                                               reply_markup=markup)
    return result

