



from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.bot.utils.navigation import NavAdmin, NavMain



def admin_keyboard():
    builder : InlineKeyboardBuilder = InlineKeyboardBuilder()
    main_menu_button = InlineKeyboardButton(text = _("main_menu:button:main"),
                                            callback_data = NavMain.MAIN)


    distrubution_button = InlineKeyboardButton(text = _("рассылка ауе всем ворам"),
                                               callback_data=NavAdmin.DISTR)

    builder.row(distrubution_button)
    builder.row(main_menu_button)
    return builder.as_markup()





def distr_example_keyboard():
    builder : InlineKeyboardBuilder = InlineKeyboardBuilder()
    main_menu_button = InlineKeyboardButton(text = _("main_menu:button:main"),
                                            callback_data = NavMain.MAIN)

    confirm_distr_button = InlineKeyboardButton(text = "confirm",
                                                callback_data=NavAdmin.CONFIRM_DISTR)
    cancel_distr_button = InlineKeyboardButton(text = "cancel", 
                                               callback_data = NavAdmin.CANCEL_DISTR)

    builder.row(confirm_distr_button)
    builder.row(cancel_distr_button)

    return builder.as_markup()



