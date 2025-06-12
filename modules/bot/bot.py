from aiogram import Bot, Dispatcher, types
import asyncio 
from configs.main_config import TELERAM_API_KEY
from aiogram.enums.parse_mode import ParseMode
from math import ceil
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from modules.yookassa_handler import Yookassa_handler
#from modules.databases.enums.users_enum import RegisterUserEnum 
from modules.yookassaAPI.yookassa_new import TransactionStatus
from modules.database.DB_GINO_MANAGER import DatabaseManager

from modules.bot.utils.navigation import NavConnect
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
        amount = transaction.amount
        await transaction.set_success()
        await self.app_manager.add_days_to_user(user_id,days)
        await self.bot.send_message(user_id, f"⚡️ Ваш баланс пополнен на <b>{amount}₽</b>.",parse_mode=ParseMode.HTML)


        user = await self.app_manager.get_user(user_id)

        if user.invited_by:
            referrer_id = user.invited_by
            bonus_days = int((days * 3)/10)
            amount_ref = int((amount * 3)/10)
            await self.app_manager.add_days_to_user(referrer_id, bonus_days)
            await self.bot.send_message(referrer_id, f"⚡️ Вам начислено <b>{amount_ref}₽</b> за пополнение вашего друга.", parse_mode=ParseMode.HTML)


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

    async def notification_checker(self):
        while True:
            try:
                users = await self.app_manager.get_users_for_notifications()
                current_time = time.time() 
                for user in users:
                    try:
                        expiry_seconds = user.expiry_time / 1000 if user.expiry_time > 1e12 else user.expiry_time
                        remaining_days = ceil((expiry_seconds - current_time) / 86400)
                        if remaining_days == 1 and not user.notify_day_before:
                            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="💸 Пополнить баланс",callback_data=NavConnect.TOPUP)]])
                            await self.bot.send_message(user.user_id,"⚠️ <b>Ваш баланс будет исчерпан завтра!</b>\n\nПополните баланс, чтобы сохранить непрерывный доступ к Sosa VPN.",parse_mode=ParseMode.HTML,reply_markup=keyboard)
                            await self.app_manager.mark_notification_sent(user.user_id, 'day_before')
                        
                        elif remaining_days == 0 and not user.notify_day:
                            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="💸 Пополнить баланс",callback_data=NavConnect.TOPUP)]])
                            await self.bot.send_message(user.user_id,"⚠️ <b>Ваш баланс исчерпан!</b>\n\nПополните баланс, чтобы восстановить доступ к Sosa VPN.",parse_mode=ParseMode.HTML,reply_markup=keyboard)
                            await self.app_manager.mark_notification_sent(user.user_id, 'day')

                        elif remaining_days < 0:
                            days_passed = abs(remaining_days)
                            if days_passed in [3, 6, 9, 12] and user.notify_day_after < (days_passed // 3):
                                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text="💸 Пополнить баланс",callback_data=NavConnect.TOPUP)]])
                                await self.bot.send_message(user.user_id,f"⚡️ <b>Вы не заходили к нам уже {days_passed} дней.</b>\n\nПополните баланс, чтобы восстановить доступ к Sosa VPN.",parse_mode=ParseMode.HTML,reply_markup=keyboard)
                                await self.app_manager.mark_notification_sent(user.user_id, 'day_after', days_passed // 3)
                    
                    except Exception as e:
                        print(f"Error sending notification to user {user.user_id}: {e}")
            
            except Exception as e:
                print(f"Notification checker error: {e}")
            
            await asyncio.sleep(5)

    async def start(self):
        asyncio.create_task(self.transaction_checker())
        asyncio.create_task(self.notification_checker())
        #asyncio.create_task(self.set_notifys())

        await self.dp.start_polling(self.bot)




