from aiogram.types import FSInputFile
from aiogram import types
import modules.bot.texts as texts
from modules.bot.keyboards import MainBotKeyboards
from modules.bot.callbacks import purshare_method_starter
import modules.bot.callbacks as callbacks

from modules.databases.enums.users_enum import RegisterUserEnum

from aiogram.enums import ParseMode
import asyncio

class Handlers():
    def __init__(self,db_manager,app_manager):
        self.sosa_vpn_banner = FSInputFile("./src/vpn_banner.jpg")
        self.keyboards = MainBotKeyboards()
        self.texts = texts
        self.db_manager = db_manager

        self.app_manager = app_manager
            

    async def start_handler(self,message: types.Message,callback):
        #TODO fix error when ref register multiple times
        #getting ids
        
        ref_id = message.text.split(" ")[1] if len(message.text.split()) > 1 else 0
        ref_id=int(ref_id)
        user_id = message.from_user.id
        print(f"{user_id} invited by {ref_id}")
        #answer 
        welcome_caption = self.texts.welcome_text
        await message.answer_photo(photo=self.sosa_vpn_banner,
                                    caption=welcome_caption,
                                    reply_markup=self.keyboards.main_keyboard)
        
        #check is user already exists
        if await self.app_manager.is_user_exists(user_id):
            return
        
        await self.app_manager.register_user(user_id)

        #register user
        # referral program
        if ref_id:
            await callback(user_id,ref_id)
            await self.app_manager.new_referral(user_id,ref_id)

              
    async def profile_handler(self,message: types.Message ,bot_username):
        user_id  = message.chat.id
        user = await self.db_manager.get_user(user_id)
        #balance  = await user.get_balance(user_id)
        refs     = await user.get_referrals()

        msg = self.texts.profile_text(refs,user_id,bot_username)
        keyboard = self.keyboards.profile_keyboard

        await message.reply(text = msg,
                            parse_mode=ParseMode.HTML,)

    async def information_handler(self,message: types.Message):
        msg = self.texts.info
        keyboard = self.keyboards.information_keyboard
        await message.reply(text = msg, reply_markup= keyboard)

    async def balance_handler(self,message:types.Message):
        msg = self.texts.gen_balance_text()
        await message.reply(text = msg)

    async def connect_vpn_handler(self, message: types.message):
        user_id = message.from_user.id
        # key = await self.db_manager.get_key(user_id)
        # balance = await self.db_manager.get_balance(user_id)
        user            = await self.db_manager.get_user(user_id)
        key             = await user.get_key()
        expiry_time     = await user.get_expiry_time()
        msg             = self.texts.gen_connect_text(key,expiry_time)
        keyboard        = self.keyboards.connect_vpn_keyboard
        
        await message.reply(text = msg,reply_markup = keyboard,parse_mode=ParseMode.HTML)
    
    async def how_to_handler(self,callback:types.CallbackQuery):
        try:
            msg = self.texts.how_to_dict[callback.data]
        except:
            msg = self.texts.how_not_found
        await callback.message.answer(msg,parse_mode=ParseMode.HTML)
        await callback.answer()

    async def select_method_handler(self,callback: types.CallbackQuery):
        method = callback.data.replace(purshare_method_starter)
        await callback.message.answer("you choosed {method}")

    async def replenishment_handler(self,callback: types.CallbackQuery):        
        keyboard = self.keyboards.purshare_method_keyboard.keyboard
        await callback.message.edit_text(text = "выберите способ оплаты",reply_markup = keyboard)

    async def select_days_handler(self,
                                    query: types.CallbackQuery,
                                    callback_data: callbacks.SelectMethodCallback):
        method = callback_data.method
        keyboard = self.keyboards.days_keyboard(method,).keyboard
        await query.message.edit_text(text = "выберите кол-во дней",
                                      reply_markup = keyboard)

        