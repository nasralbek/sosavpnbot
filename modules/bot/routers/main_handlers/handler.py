from aiogram import Router
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from .keyboard import invite_keyboard,connect_vpn_keyboard,information_keyboard

from modules.bot.utils.navigation import NavMain
from .texts import profile_text, connect_text,information_text



class Handler():
    def __init__(self,app_manager):
            self.router = Router(name=__name__)
            self.bot_username = "bot_username"
            self.app_manager = 'app_manager'

            self._register_handlers()

    async def invite_friend(self,message: types.Message):
        user_id  = message.chat.id
        user = await self.app_manager.get_user(user_id)

        msg = profile_text(user,self.bot_username)
        await message.reply(text = msg,
                            parse_mode=ParseMode.HTML)

    async def information(self,message: types.Message):
        msg = information_text
        keyboard = information_keyboard().get()
        await message.reply(text = msg, reply_markup= keyboard)
    
    async def connect(self,message: types.Message):
        
        user_id = message.from_user.id
        user            = await self.app_manager.get_user(user_id)
        key             = await user.get_key()
        expiry_time     = user.expiry_time
        msg             = connect_text(key,expiry_time)
        keyboard        = connect_vpn_keyboard().get()
        
        await message.reply(text = msg,reply_markup = keyboard,parse_mode=ParseMode.HTML)



    def _register_handlers(self):
        print("initializing invite")
        self.router.message(
              lambda message: message.text == NavMain.INVITE
        )(self.invite_friend)

        print("initializing connect")
        self.router.message(
        lambda message: message.text == NavMain.CONNECT
        )(self.connect)

        print("initializing information")
        self.router.message(
        lambda message: message.text == NavMain.INFORMATION
        )(self.information)

        print("initializing invite,connect,information successfull")