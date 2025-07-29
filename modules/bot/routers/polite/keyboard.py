



from aiogram.types import InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config
from modules.bot.utils.navigation import NavMain


def polite_keyboard(config: Config):
    builder = InlineKeyboardBuilder()

    polite_button = InlineKeyboardButton(text = _("polite:button:polite"),url = config.bot.POLITE_URL)
    rules_button  = InlineKeyboardButton(text = _("polite:button:rules"), url = config.bot.RULES_URL)
    
    builder.row(polite_button)
    builder.row(rules_button)
    builder.row(InlineKeyboardButton(text=_("main_menu:button:main"), callback_data=NavMain.MAIN))

    return builder.as_markup() 
