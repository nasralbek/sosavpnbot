from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.bot.utils.navigation import (NavMain)

def invite_keyboard() -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    main_menu_button_text  = _("main_menu:button:main") 
    main_menu_button  = InlineKeyboardButton(text=main_menu_button_text,callback_data=NavMain.MAIN)
    builder.row(main_menu_button)

    return builder.as_markup()


