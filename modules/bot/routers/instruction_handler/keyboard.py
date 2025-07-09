import logging
from aiogram.types import   (ReplyKeyboardMarkup,KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton, )
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


from config import Config
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

sub_route: dict[platformEnum,str] = {
    platformEnum.IOS        : "v2raytun",
    platformEnum.ANDROID    : "happ",
    platformEnum.WINDOWS    : "happ",
    platformEnum.MACOS      : "happ",
    platformEnum.ANDROIDTV  : "v2raytun",
    platformEnum.LINUX      : "happ",
}


logger = logging.getLogger(__name__)

def get_download_button(platform : platformEnum):
    text = _("how_to:button:download")
    return InlineKeyboardButton(text = text, url = downloads[platform] )


def get_add_button(platform : platformEnum,
                   key:str,
                   sub_path:str):
    text = _("how_to:button:add")
    sub_id = "sub_id"
    url = f"{sub_path}{sub_route[platform]}/{key}"
    logger.info(url)
    return InlineKeyboardButton(text = text, url = url )

def how_to_keyboard(platform : platformEnum,config: Config, key = "") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(get_download_button(platform))
    sub_path = config.remnawave.SUBSCRIPTION_PATH
    builder.row(get_add_button(platform,key = key,sub_path = sub_path))

    builder.row(InlineKeyboardButton(text = "main_menu",callback_data = NavMain.MAIN))
    return builder.as_markup()

