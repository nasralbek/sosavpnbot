from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.bot.callbacks import HowToCallback, platformEnum
from modules.bot.routers import main_menu
from modules.bot.utils.navigation import NavMain









def connect_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    main_menu_button = InlineKeyboardButton(text=_("main_menu:button:main"),callback_data=NavMain.MAIN)

    ios         = InlineKeyboardButton(text = _("how_to:button:IOS"),
                callback_data = HowToCallback(platform = platformEnum.IOS).pack())
    android     = InlineKeyboardButton(text = _("how_to:button:ANDROID")
                , callback_data = HowToCallback(platform = platformEnum.ANDROID).pack())
    windows     = InlineKeyboardButton(text = _("how_to:button:WINDOWS")
                , callback_data = HowToCallback(platform = platformEnum.WINDOWS).pack())
    macos       = InlineKeyboardButton(text = _("how_to:button:MACOS")
                , callback_data = HowToCallback(platform = platformEnum.MACOS).pack())
    andriod_tv  = InlineKeyboardButton(text = _("how_to:button:ANDROIDTV")
                , callback_data = HowToCallback(platform = platformEnum.ANDROIDTV).pack())
    linux       = InlineKeyboardButton(text = _("how_to:button:LINUX")
                , callback_data = HowToCallback(platform = platformEnum.LINUX).pack())
    
    builder.row(ios ,        android)
    builder.row(windows ,    macos)
    builder.row(andriod_tv , linux)

    builder.row(main_menu_button)

    return builder.as_markup()
