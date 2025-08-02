from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config
from modules.bot.utils.navigation import (NavMain)

def invite_keyboard(config: Config) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    support_button  = InlineKeyboardButton(text=_("support:button:get_support"),url = f"t.me/{config.bot.SUPPORT_TAG}") 
    main_menu_button  = InlineKeyboardButton(text=_("main_menu:button:main"),callback_data=NavMain.MAIN)
    builder.row(support_button)
    builder.row(main_menu_button)


    return builder.as_markup()

