import logging
from aiogram.types import   (ReplyKeyboardMarkup,KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton, )
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


from config import Config
from modules.bot.callbacks import platformEnum
from modules.bot.utils.navigation import NavInstruction, NavMain
 

downloads: dict[platformEnum,str] = {
    platformEnum.IOS        : "https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973",
    platformEnum.ANDROID    : "https://play.google.com/store/apps/details?id=com.happproxy",
    platformEnum.WINDOWS    : "https://github.com/Happ-proxy/happ-desktop/releases/download/0.2.3_alpha/setup-Happ.x86.exe",
    platformEnum.MACOS      : "https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973",
    platformEnum.ANDROIDTV  : "https://url.com",
    platformEnum.LINUX      : "https://github.com/Happ-proxy/happ-desktop/releases/download/0.2.3_alpha/Happ.linux.x86.AppImage",
}


alt_downloads: dict[platformEnum, str] = {
    platformEnum.IOS: "https://apps.apple.com/us/app/happ-proxy-utility/id6504287215",  
    platformEnum.MACOS: "https://apps.apple.com/us/app/happ-proxy-utility/id6504287215",
}


sub_route: dict[platformEnum,str] = {
    platformEnum.IOS        : "happ://add",
    platformEnum.ANDROID    : "happ://add",
    platformEnum.WINDOWS    : "happ://add",
    platformEnum.MACOS      : "happ://add",
    platformEnum.ANDROIDTV  : "happ://add",
    platformEnum.LINUX      : "happ://add",
}



logger = logging.getLogger(__name__)

def get_download_button(platform : platformEnum):
    text = _("how_to:button:download")
    if platform in [platformEnum.IOS, platformEnum.MACOS]:
        text = _("how_to:button:download_apple")
    return InlineKeyboardButton(text = text, url = downloads[platform] )


def get_alt_download_button(platform: platformEnum):
    if platform not in alt_downloads:
        return None
    text = _("how_to:button:download_apple_alt")
    return InlineKeyboardButton(text=text, url=alt_downloads[platform])


def get_add_button(platform : platformEnum,
                   key:str,
                   sub_path:str):
    text = _("how_to:button:add")
    sub_id = "sub_id"
    deeplink_path = "https://sosa.ink/"
    url = f"{deeplink_path}?url={sub_route[platform]}/{sub_path}{key}"
    logger.info(url)
    return InlineKeyboardButton(text = text, url = url )

def how_to_keyboard(platform : platformEnum,config: Config, key = "") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(get_download_button(platform))
    
    
    if platform in [platformEnum.IOS, platformEnum.MACOS]:
        alt_button = get_alt_download_button(platform)
        if alt_button:
            builder.row(alt_button)


    sub_path = config.remnawave.SUBSCRIPTION_PATH
    builder.row(get_add_button(platform,key = key,sub_path = sub_path))
    text = _("main_menu:button:main")
    builder.row(InlineKeyboardButton(text = text,callback_data = NavMain.MAIN))
    return builder.as_markup()

