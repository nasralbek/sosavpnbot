
from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.bot.utils.navigation import NavMain


def purshare_final_keyboard(pay_url : str ):
    builder = InlineKeyboardBuilder()

    main_menu_button = InlineKeyboardButton(text=_("main_menu:button:main"),
                                            callback_data=NavMain.MAIN)

    pay_button = InlineKeyboardButton(text = _("purschare_final:button:pay"),
                                      url = pay_url)
    builder.row(pay_button)
    builder.row(main_menu_button)
    return builder.as_markup()
