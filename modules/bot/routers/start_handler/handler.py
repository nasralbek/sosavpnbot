from aiogram import Router,types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.enums.parse_mode import ParseMode

from modules.bot.utils.navigation import NavMain

from .texts import welcome_text
from .keyboard import main_keyboard 


class Handler():
    def __init__(self,app_manager,bot):
            self.router = Router(name=__name__)
            self.app_manager = app_manager
            self.bot = bot
            self.sosa_vpn_banner = FSInputFile("./src/vpn_banner.jpg")
            self._register_handlers()


    async def register_user_notify(self,user_id,ref_id):
        await self.bot.send_message(user_id,
                                    "🎉 Вы зарегистрировались по реферальной ссылке! <b>Вам начислено 50₽.</b>",
                                    parse_mode=ParseMode.HTML)
        await self.bot.send_message(ref_id, 
                                    "🎉 Ваш друг зарегистрировался по реферальной ссылке! <b>Вам начислено 24₽.</b>",
                                    parse_mode=ParseMode.HTML)

    async def start(self,message: types.Message):
        #TODO fix error when ref register multiple times
        #getting ids
        
        ref_id = message.text.split(" ")[1] if len(message.text.split()) > 1 else 0
        ref_id=int(ref_id)
        user_id = message.from_user.id
        print(f"{user_id} invited by {ref_id}")

        welcome_caption = welcome_text
        await message.answer_photo(photo=self.sosa_vpn_banner,
                                    caption=welcome_caption,
                                    reply_markup=main_keyboard,
                                    parse_mode=ParseMode.HTML)
        
        #check is user already exists
        if await self.app_manager.is_user_exists(user_id):
            return
        
        await self.app_manager.register_user(user_id)

        #register user
        # referral program
        if ref_id:
            await self.register_user_notify(user_id,ref_id)
            await self.app_manager.new_referral(user_id,ref_id)

    def _register_handlers(self):
        print("initializing start handler")
        self.router.message(
              Command(NavMain.MAIN)
        )(self.start)
