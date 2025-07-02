import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from modules.bot.callbacks import SelectMethodCallback
from modules.bot.models.purchase_data import PurchaseData
from modules.bot.models.services_container import ServicesContainer
from modules.bot.payment_gateways import GatewayFactory
from .keyboard import purshare_final_keyboard
from modules.bot.utils.navigation import NavPurshare
from modules.database.models.user import User
from modules.utils.constants import (PREVIOUS_CALLBACK_KEY,
                                    SELECTED_DAYS_KEY,
                                    SELECTED_METHOD_KEY,
                                    SELECTED_PLAN_KEY,
                                    SELECTED_PRICE_KEY)


logger = logging.getLogger(__name__)
router = Router(name=__name__)

async def prepare_message(days,price,method,url) ->str:
    return f"you want to buy {days} days by {price}rub with {method},\n\
    your purshare url: {url}"

@router.callback_query(F.data == NavPurshare.CONFIRM)
async def purshare_final(callback       : CallbackQuery,
                        user            : User,
                        state           : FSMContext,
                        services        : ServicesContainer,
                        config          : Config,
                        session         : AsyncSession,
                        gateway_factory : GatewayFactory):
    logger.info(f"User {user.tg_id} opened invite page.")

    try:
        days    = await state.get_value(SELECTED_DAYS_KEY)
        price   = await state.get_value(SELECTED_PRICE_KEY)
        method  = await state.get_value(SELECTED_METHOD_KEY)
        name    = await state.get_value(SELECTED_PLAN_KEY)

        logger.info(f"user {user.tg_id} create payment : \n\
                        method: {method}\n\
                        price: {price} rub\n\
                        days: {days}\n")
        gateway = gateway_factory.get_gateway(method)

        pay_url = await gateway.create_payment(PurchaseData(user_id   = user.tg_id,
                                                      name      = name,
                                                      days      = days,
                                                      price     = price,
                                                      )) 
        text = await prepare_message(days,price,method,pay_url)
        markup = purshare_final_keyboard()
        result =  await callback.message.edit_text(text=text,
                                               reply_markup=markup)
        return result
    except Exception as e:
        logger.error(e)
    return None

