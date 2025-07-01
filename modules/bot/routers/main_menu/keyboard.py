from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.bot.utils.navigation import (NavConnect,NavInvite,NavSupport,NavAdmin)

def main_menu_keyboard(is_admin : bool = False,
                       is_refferal_avaible: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    invite_text     = _("main_menu:button:invite_friend")
    connect_text  = _("main_menu:button:profile") 
    support_text  = _("main_menu:button:support") 

    connect_button  = InlineKeyboardButton(text=connect_text,callback_data=NavConnect.MAIN)
    invite_button   = InlineKeyboardButton(text=invite_text ,callback_data=NavInvite.MAIN)
    support_button  = InlineKeyboardButton(text=support_text,callback_data=NavSupport.MAIN) 
    admin_button    = InlineKeyboardButton(text='adm'       ,callback_data=NavAdmin.MAIN)

    builder.row(connect_button)
    builder.row(*([invite_button] if is_refferal_avaible else []),support_button)
    
    if is_admin:
        builder.row(admin_button)

    return builder.as_markup()

