from aiogram.filters import callback_data

from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.bot.utils.navigation import NavMain
from modules.bot.models import Plan
from modules.bot.callbacks import SelectPlanCallback


def purshare_keyboard(plans : list[Plan])-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for p in plans:
        text = _("select_plan:button:text").format(days = p.days, price = p.price)
        callback_data = SelectPlanCallback(days     = p.days,
                                           price    = p.price,
                                           name     = p.name).pack()
        builder.row(
            InlineKeyboardButton(text=text,callback_data = callback_data)
        )
    builder.row(InlineKeyboardButton(text=_("main_menu:button:main"), callback_data=NavMain.MAIN))

    return builder.as_markup()
