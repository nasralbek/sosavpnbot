from aiogram import Router,types,F
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import FSInputFile

from modules.bot.utils.filters import InstructionFilter,HowToFilter
from modules.bot.utils.navigation import NavInstruction

from .texts import instructions_text,how_to_dict
from .keyboard import instruction_keyboard,how_to_keyboard


class Handler():
    def __init__(self,app_manager):
            self.router = Router(name=__name__)
            self.app_manager = app_manager
            self.sosa_vpn_banner = FSInputFile("./src/vpn_banner.jpg")
            self._register_handlers()

    async def get_sub_id(self,user_id):
        user = await self.app_manager.get_user(user_id)
        return user.sub_id


    async def instructions(self,callback: types.CallbackQuery):
        keyboard = instruction_keyboard
        text = instructions_text
        await callback.message.edit_text(text = text,parse_mode=ParseMode.HTML,reply_markup = keyboard)

    def get_download_url(self,callback_data):
        download_links = {
            NavInstruction.ANDROID : 'https://play.google.com/store/apps/details?id=com.v2raytun.android',
            NavInstruction.MAC     : 'https://github.com/hiddify/hiddify-next/releases/latest/download/Hiddify-MacOS.dmg',
            NavInstruction.IOS     : 'https://apps.apple.com/us/app/v2raytun/id6476628951',
            NavInstruction.WIDNOWS : 'https://github.com/hiddify/hiddify-next/releases/latest/download/Hiddify-Windows-Setup-x64.exe',
            NavInstruction.LINUX   : 'https://github.com/hiddify/hiddify-app/releases/latest/download/Hiddify-Linux-x64.AppImage'
        }
        return download_links[callback_data]


    async def how_to(self,callback: types.CallbackQuery):
        user_id = callback.from_user.id
        sub_id = await self.get_sub_id(user_id)
        href_start = 'https://add.sosavpn.tech/import'
        if callback.data == NavInstruction.IOS or callback.data == NavInstruction.ANDROID:
            app_name = 'V2RayTun'
        else:
            app_name = 'Hiddify'
        href = f'{href_start}/{app_name}/{sub_id}'
        download_url = self.get_download_url(callback.data)
        try:
            msg = how_to_dict[callback.data]
        except Exception as e:
            print(e)
            msg = 'not_found'
        
        keyboard = how_to_keyboard(app_name,deeplink=href,download_url=download_url)

        await callback.message.edit_text(msg,parse_mode=ParseMode.HTML,reply_markup=keyboard)
        await callback.answer()

    def _register_handlers(self):
        print("initializing instructions handler")
        self.router.callback_query(InstructionFilter()) (self.instructions)
        self.router.callback_query(HowToFilter()) (self.how_to)





