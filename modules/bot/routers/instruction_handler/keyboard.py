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
    platformEnum.IOS        : "https://apps.apple.com/us/app/v2raytun/id6476628951",
    platformEnum.ANDROID    : "https://play.google.com/store/apps/details?id=com.v2raytun.android",
    platformEnum.WINDOWS    : "https://github.com/Happ-proxy/happ-desktop/releases/download/0.1.2_alpha/setup-Happ.x86.exe",
    platformEnum.MACOS      : "https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973",
    platformEnum.ANDROIDTV  : "https://url.com",
    platformEnum.LINUX      : "https://github.com/hiddify/hiddify-next/releases/download/v2.5.7/Hiddify-Linux-x64.AppImage",
}

sub_route: dict[platformEnum,str] = {
    platformEnum.IOS        : "v2raytun://import",
    platformEnum.ANDROID    : "v2raytun://import",
    platformEnum.WINDOWS    : "happ://add",
    platformEnum.MACOS      : "happ://add",
    platformEnum.ANDROIDTV  : "v2raytun://import",
    platformEnum.LINUX      : "happ://add",
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
    url = f"{sub_path}?url={sub_route[platform]}/{sub_path}sub/{key}"
    logger.info(url)
    return InlineKeyboardButton(text = text, url = url )

def how_to_keyboard(platform : platformEnum,config: Config, key = "") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(get_download_button(platform))
    sub_path = config.remnawave.SUBSCRIPTION_PATH
    builder.row(get_add_button(platform,key = key,sub_path = sub_path))
    text = _("main_menu:button:main")
    builder.row(InlineKeyboardButton(text = text,callback_data = NavMain.MAIN))
    return builder.as_markup()

