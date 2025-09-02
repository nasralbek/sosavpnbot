from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config
from modules.bot.utils.navigation import (NavPolite, NavProfile,NavInvite, NavPurshare,NavSupport,NavAdmin)

def main_menu_keyboard(     config              : Config,
                            is_admin            : bool = False,
                            is_refferal_avaible : bool = False,
                       ) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    invite_text     = _("main_menu:button:invite_friend")
    connect_text    = _("main_menu:button:profile") 
    support_text    = _("main_menu:button:support") 
    purshare_text   = _("main_menu:button:purshare")
    polite_text     = _("main_menu:button:polite")



    connect_button  = InlineKeyboardButton(text=connect_text,callback_data=NavProfile.MAIN)
    purshare_button = InlineKeyboardButton(text=purshare_text,callback_data=NavPurshare.MAIN)
    invite_button   = InlineKeyboardButton(text=invite_text ,callback_data=NavInvite.MAIN)
    support_button  = InlineKeyboardButton(text=support_text,callback_data = NavSupport.MAIN) 
    polite_button   = InlineKeyboardButton(text=polite_text,callback_data = NavPolite.MAIN) 
        
    admin_button    = InlineKeyboardButton(text='adm'       ,callback_data=NavAdmin.MAIN)
    #rules_button    = InlineKeyboardButton(text='📝 О сервисе', url='https://telegra.ph/Usloviya-servisa-Sosa-VPN-07-29')
    rauf_button     = InlineKeyboardButton(text = "rauf",url="https://t.me/tribute/app?startapp=szzE")

    builder.row(connect_button)
    builder.row(purshare_button)
    builder.row(*([invite_button] if is_refferal_avaible else []),support_button)
    builder.row(polite_button)
    builder.row(rauf_button)
    #builder.row(rules_button)
    
    if is_admin:
        builder.row(admin_button)

    return builder.as_markup()

