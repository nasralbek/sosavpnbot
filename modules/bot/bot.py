from aiogram import Bot, Dispatcher, types
import asyncio 
from configs.main_config import TELERAM_API_KEY

#from modules.yookassa_handler import Yookassa_handler
#from modules.databases.enums.users_enum import RegisterUserEnum 
from modules.yookassaAPI.yookassa_new import TransactionStatus
from modules.database.DB_GINO_MANAGER import DatabaseManager
from modules.bot.handlers import Handlers 
from modules.bot.keyboard_texts import MainKeyboardTexts
import modules.bot.callbacks as callbacks


class vpnBot():
    def __init__(self,app_manager):
        self.bot = Bot(TELERAM_API_KEY)
        self.dp = Dispatcher() 
        self.app_manager = app_manager 

        self.init_bot_handlers()

    async def register_user_notify(self,user_id,ref_id):
            await self.bot.send_message(user_id,"you have been registered by ref")
            await self.bot.send_message(ref_id, "some one registered by ref")
    
    def init_bot_handlers(self):
        self.handlers = Handlers(self.app_manager)
        @self.dp.message(lambda message: message.text.startswith("/start"))
        async def start_handler(message):
            async def callback(user_id,ref_id):
                await self.register_user_notify(user_id,ref_id)
            await self.handlers.start_handler(message,callback)

        @self.dp.message(lambda message: message.text == MainKeyboardTexts.profile_text )
        async def profile_handler(message :types.Message ):
            await self.handlers.profile_handler(message,(await self.bot.get_me()).username)

        
        @self.dp.message(lambda message: message.text == MainKeyboardTexts.information_text)
        async def information_handler(message: types.Message):
            await self.handlers.information_handler(message)
        
        @self.dp.message(lambda message: message.text == MainKeyboardTexts.balance_text)
        async def balance_handler(message: types.Message):
            print("balance")
            await self.handlers.balance_handler(message)

        @self.dp.message(lambda message: message.text == MainKeyboardTexts.connect_vpn_text)
        async def connect_vpn_handler(message: types.Message):
            print("connect")
            await self.handlers.connect_vpn_handler(message)

        @self.dp.callback_query(lambda callback: callback.data in callbacks.how_to_callbacks.list )
        async def how_to_handler(callback: types.CallbackQuery):
            await self.handlers.how_to_handler(callback)

        @self.dp.callback_query(lambda callback: callback.data == callbacks.replenishment_callback )
        async def replenishment_handler(callback: types.CallbackQuery):
            print("replenishment handler")
            await self.handlers.replenishment_handler(callback)

        @self.dp.callback_query(callbacks.SelectMethodCallback.filter())
        async def select_method_handler(query: types.CallbackQuery,callback_data: types.CallbackQuery):
            print("method handler")
            await self.handlers.select_method_handler(query,callback_data)

        @self.dp.callback_query(callbacks.SelectDaysCallback.filter())
        async def select_days_handler(query: types.CallbackQuery,callback_data: types.CallbackQuery):
            print("days handler")
            await self.handlers.select_days_handler(query,callback_data)

        @self.dp.callback_query(callbacks.ConfirmCallback.filter())
        async def confirm_handler(query: types.CallbackQuery,callback_data: types.CallbackQuery):
            print("confirm handler")
            await self.handlers.confirm_handler(query,callback_data)

        @self.dp.callback_query(callbacks.InstructionsCallback.filter())
        async def instructions_handler(query: types.CallbackQuery, callback_data: callbacks.InstructionsCallback):
            print("instructions")
            await self.handlers.instructions_handler(query,callback_data)

    async def on_transaction_success(self,transaction):
        user_id = transaction.user_id
        days = transaction.days
        await transaction.set_success()
        await self.app_manager.add_days_to_user(user_id,days)
        await self.bot.send_message(user_id, f"пополение на {days} дней успешно")


    async def on_transaction_canceled(self,transaction):
        await transaction.set_canceled()

    async def transaction_checker(self):
        while True:
            transactions = await self.app_manager.get_pending_transactions()
            for transaction in transactions:
                try:
                    payment_id = transaction.payment_id
                    status = self.app_manager.check_transaction(payment_id) #status
                    if status == TransactionStatus.success:
                        await self.on_transaction_success(transaction)
                    elif status == TransactionStatus.canceled:
                        await self.on_transaction_canceled(transaction)
                except Exception as e:
                    print(e)
            await asyncio.sleep(5)

    async def start(self):
        asyncio.create_task(self.transaction_checker())
        await self.dp.start_polling(self.bot)




