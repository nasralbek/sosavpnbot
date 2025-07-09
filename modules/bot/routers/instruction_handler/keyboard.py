from aiogram.types import   (ReplyKeyboardMarkup,KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton, )
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


from modules.bot.callbacks import platformEnum
from modules.bot.utils.navigation import NavInstruction, NavMain

# connect_button      = KeyboardButton(text=NavMain.CONNECT,      )
# information_button  = KeyboardButton(text=NavMain.INFORMATION,  )
# invite_button       = KeyboardButton(text=NavMain.INVITE,       )  

downloads: dict[platformEnum,str] = {
    platformEnum.IOS        : "https://url.com",
    platformEnum.ANDROID    : "https://url.com",
    platformEnum.WINDOWS    : "https://url.com",
    platformEnum.MACOS      : "https://url.com",
    platformEnum.ANDROIDTV  : "https://url.com",
    platformEnum.LINUX      : "https://url.com",
}

sublinks: dict[platformEnum,str] = {
    platformEnum.IOS        : "https://url.com/",
    platformEnum.ANDROID    : "https://url.com/",
    platformEnum.WINDOWS    : "https://url.com/",
    platformEnum.MACOS      : "https://url.com/",
    platformEnum.ANDROIDTV  : "https://url.com/",
    platformEnum.LINUX      : "https://url.com/",
}


def get_download_button(platform : platformEnum):
    text = _("how_to:button:download")
    return InlineKeyboardButton(text = text, url = downloads[platform] )


def get_add_button(platform : platformEnum):
    text = _("how_to:button:add")
    sub_id = "sub_id"
    return InlineKeyboardButton(text = text, url = sublinks[platform] + sub_id )

def how_to_keyboard(platform : platformEnum) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(get_download_button(platform))
    builder.row(get_add_button(platform))

    builder.row(InlineKeyboardButton(text = "main_menu",callback_data = NavMain.MAIN))
    return builder.as_markup()

