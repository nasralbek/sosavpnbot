from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


def connect_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    purchase_button = InlineKeyboardButton(text = "buy",callback_data="buy")

    builder.row(purchase_button)

    return builder.as_markup()