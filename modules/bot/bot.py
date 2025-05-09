from aiogram import Bot, Dispatcher, types
import asyncio 
from configs.main_config import TELERAM_API_KEY

#from modules.yookassa_handler import Yookassa_handler
#from modules.databases.enums.users_enum import RegisterUserEnum 
from modules.yookassaAPI.yookassa_new import TransactionStatus
from modules.database.DB_GINO_MANAGER import DatabaseManager

import modules.bot.callbacks as callbacks
from .routers import include_routers


class vpnBot():
    def __init__(self,app_manager):
        self.bot = Bot(TELERAM_API_KEY)
        self.dp = Dispatcher() 
        self.app_manager = app_manager 

        asyncio.create_task(include_routers(self.bot,self.dp,self.app_manager))


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




