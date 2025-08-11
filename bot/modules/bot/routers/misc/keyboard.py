from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from modules.bot.utils.navigation import NavMain


def close_notification_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text= _("misc:button:close_notification"),
        callback_data=NavMain.CLOSE_NOTIFICATION,
    )

def close_notification_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(close_notification_button())
    return builder.as_markup()