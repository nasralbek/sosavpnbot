from aiogram.types import   (ReplyKeyboardMarkup,KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton, )
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from modules.bot.utils.navigation import NavMain
from aiogram.utils.i18n import gettext as _

connect_button      = KeyboardButton(text=NavMain.CONNECT,      )
information_button  = KeyboardButton(text=NavMain.INFORMATION,  )
invite_button       = KeyboardButton(text=NavMain.INVITE,       )  

# main_keyboard = ReplyKeyboardMarkup(keyboard=
#     [
#         [connect_button ],
#         [
#             invite_button,
#             information_button,
#         ]
#     ],resize_keyboard=True)


def main_menu_keyboard(
        is_admin: bool = False,
        is_referral_avaible: bool = False,
):
    builder = ReplyKeyboardBuilder()
    
    connect_button      = KeyboardButton(text=_("main_menu:button:connect_vpn"))
    information_button  = KeyboardButton(text=_("main_menu:button:information"))
    invite_button       = KeyboardButton(text=_("main_menu:button:invite_friend"))
    admin_button        = KeyboardButton(text=_("main_menu:button:admin"))

    builder.row(connect_button)
    second_row = []
    if is_referral_avaible:
        second_row.append(invite_button)
    second_row.append(information_button)
    builder.row(
        *second_row
    )

    
    if is_admin:
        builder.row(admin_button)


    return builder.as_markup(resize_keyboard=True)
