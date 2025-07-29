
from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config
from modules.bot.callbacks import SelectMethodCallback
from modules.bot.utils.navigation import NavMain, NavPurshare


def select_method_keyboard(config : Config) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    yooKassaButton = InlineKeyboardButton(text=_("purschare:method:pay_yookassa"),
                    callback_data = SelectMethodCallback(
                                          method_key=NavPurshare.PAY_YOOKASSA
                                          ).pack())
    heleketButton = InlineKeyboardButton(text = _("purschare:method:pay_heleket"),
                                         callback_data = SelectMethodCallback(
                                         method_key=NavPurshare.PAY_HELEKET).pack())
    main_menu_button = InlineKeyboardButton(text=_("main_menu:button:main"),callback_data=NavMain.MAIN)

    if config.shop.PAYMENT_YOOKASSA_ENABLED:
        builder.row(yooKassaButton)
    if config.shop.PAYMENT_HELEKET_ENABLED:
        builder.row(heleketButton)

    builder.row(main_menu_button)

    return builder.as_markup()
