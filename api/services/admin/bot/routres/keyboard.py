from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.admin.bot.navigation import NavMain


def admin_keyboard():

    node_status_button = InlineKeyboardButton(text="Node Status", callback_data=NavMain.NODE_STATUS)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                    [node_status_button],

                                             ])
    return keyboard
