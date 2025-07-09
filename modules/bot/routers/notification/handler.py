

import logging

from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery 
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from modules.bot.models.services_container import ServicesContainer
from modules.bot.utils.navigation import NavNotify
from modules.database.models.user import User


router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == NavNotify.CLOSE)
async def close_notify(callback    : CallbackQuery,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession):
    message_id = callback.message.message_id
    logger.info(f"user {user.tg_id} closed notification : {message_id}")
    await callback.bot.delete_message(chat_id       = user.tg_id,
                                      message_id    = message_id)

    
