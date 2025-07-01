from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.bot.routers import main_menu
from modules.bot.utils.navigation import NavMain


def connect_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    purchase_button = InlineKeyboardButton(text = "buy",callback_data="buy")
    main_menu_button = InlineKeyboardButton(text="main_menu",callback_data=NavMain.MAIN)

    builder.row(purchase_button)
    builder.row(main_menu_button)

    return builder.as_markup()
