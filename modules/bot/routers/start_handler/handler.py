from aiogram import Router,types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.enums.parse_mode import ParseMode

from modules.bot.utils.navigation import NavMain

from .texts import welcome_text, trial_text
from .keyboard import main_keyboard 


class Handler():
    def __init__(self,app_manager,bot):
            self.router = Router(name=__name__)
            self.app_manager = app_manager
            self.bot = bot
            self.sosa_vpn_banner = FSInputFile("./src/vpn_banner.jpg")
            self._register_handlers()


    async def register_user_notify(self,ref_id):
        await self.bot.send_message(ref_id, 
                                    "⚡️ Ваш друг зарегистрировался по вашей ссылке!",
                                    parse_mode=ParseMode.HTML)

    async def start(self, message: types.Message):
        try:
            ref_id = 0
            if len(message.text.split()) > 1:
                try:
                    ref_id = int(message.text.split()[1])
                    if ref_id == message.from_user.id:
                        ref_id = 0
                except ValueError:
                    ref_id = 0

            user_id = message.from_user.id
            user_exists = await self.app_manager.is_user_exists(user_id)
            ref_exists = await self.app_manager.is_user_exists(ref_id)

            if user_exists:
                await message.answer(
                    text=welcome_text,
                    reply_markup=main_keyboard,
                    parse_mode=ParseMode.HTML
                )
            else:
                await self.app_manager.register_user(user_id)
                await message.answer(
                    text=trial_text,
                    reply_markup=main_keyboard,
                    parse_mode=ParseMode.HTML
                )
                if ref_id and ref_exists:
                    await self.register_user_notify(ref_id)
                    await self.app_manager.new_referral(user_id, ref_id)
                    print(f"{user_id} invited by {ref_id}")


        except Exception as e:
            print(f"Error in start handler: {e}")
            await message.answer("⚠️ Произошла ошибка, попробуйте позже")

    def _register_handlers(self):
        print("initializing start handler")
        self.router.message(
              Command(NavMain.MAIN)
        )(self.start)
