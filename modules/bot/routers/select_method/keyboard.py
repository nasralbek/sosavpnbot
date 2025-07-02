

from aiogram.utils.i18n import gettext as _
from aiogram.filters import callback_data
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.bot.utils.navigation import NavMain, NavPurshare


def confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    main_menu_button    = InlineKeyboardButton(text = _("main_menu:button:main"),
                                            callback_data=NavMain.MAIN) 
    confirm_button      = InlineKeyboardButton(text = _("confirm:button:main"),
                                            callback_data = NavPurshare.CONFIRM)

    builder.row(confirm_button)
    builder.row(main_menu_button)


    return builder.as_markup()
