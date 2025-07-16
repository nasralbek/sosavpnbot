
import logging
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, message_id
from aiogram.types.message import Message

from config import Config
from modules.bot.filters import is_admin
from modules.bot.filters.is_admin import IsAdmin
from modules.bot.models.services_container import ServicesContainer
from modules.bot.routers.admin_tools.keyboard import admin_keyboard, distr_example_keyboard 
from modules.bot.routers.main_menu.handler import redirect_to_main_menu
from modules.bot.utils.navigation import NavAdmin
from modules.database.models.user import User
from modules.utils.constants import MAIN_MESSAGE_ID_KEY, PREVIOUS_MESSAGE_ID_KEY, SAVED_TEXT_KEY
from tools.image_container import ImageContainer

import random




logger = logging.getLogger(__name__)
router = Router(name=__name__)




@router.callback_query(F.data == NavAdmin.MAIN, IsAdmin() )
async def admin_tools(
    callback: CallbackQuery,
    user: User,
    services: ServicesContainer,
    state: FSMContext,
    config: Config,
    images: ImageContainer
):
    return await callback.message.edit_caption(caption = "adminka" + f"{random.randint(0,321)}",
                                               reply_markup = admin_keyboard())



@router.message(IsAdmin())
async def handle_distr(
    message: Message,
    user: User,
    services: ServicesContainer,
    state: FSMContext,
    config: Config,
    images: ImageContainer
):
    main_message_id = await state.get_value(MAIN_MESSAGE_ID_KEY)
    try:
        if main_message_id:
            await message.bot.delete_message(chat_id = message.chat.id,message_id=main_message_id)
    except Exception as e:
        logger.exception(e)
    text = message.text
    return message.answer(text = message.html_text,reply_markup = distr_example_keyboard() )



@router.callback_query(F.data == NavAdmin.CONFIRM_DISTR, IsAdmin())
async def handle_confirm_distr(
    callback: CallbackQuery,
    user: User,
    services: ServicesContainer,
    state: FSMContext,
    config: Config,
    images: ImageContainer
):
    await callback.message.delete()
    text = callback.message.html_text
    await services.notification.notify_all(text = text,executer = user)
    return await callback.message.delete()
    #start_distr




@router.callback_query(F.data == NavAdmin.CANCEL_DISTR, IsAdmin())
async def handle_cancel_distr(
    callback: CallbackQuery,
    user: User,
    services: ServicesContainer,
    state: FSMContext,
    config: Config,
    images: ImageContainer
):
    logger.info("distr_cancel")
    await callback.message.delete()
    return await redirect_to_main_menu(
        bot = callback.message.bot,
        user = user,
        services = services,
        config = config,
        images = images,
        state = state,
    )



