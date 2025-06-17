from aiogram import Bot, Dispatcher, types
import asyncio 
from configs.main_config import TELERAM_API_KEY
from aiogram.enums.parse_mode import ParseMode
from math import ceil
import time
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from modules.yookassa_handler import Yookassa_handler
#from modules.databases.enums.users_enum import RegisterUserEnum 
from modules.yookassaAPI.yookassa_new import TransactionStatus
from modules.database.DB_GINO_MANAGER import DatabaseManager
from modules.xuiAPI.xuiAPI import X_UI_API

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
        await self.bot.send_message(user_id, f"⚡️ <b>Ваш баланс пополнен на {days} дней.</b>\n\n"
                                            "⚙️ <b>Для управления балансом перейдите в личный кабинет по кнопке в главном меню.</b>\n\n"
                                            "• Открыть главное меню: /start",
                                    parse_mode=ParseMode.HTML)


        user = await self.app_manager.get_user(user_id)

        if user.invited_by:
            referrer_id = user.invited_by
            bonus_days = int(10)
            #amount_ref = int((amount * 3)/10)
            await self.app_manager.add_days_to_user(referrer_id, bonus_days)
            await self.bot.send_message(referrer_id, f"⚡️ <b>Ваш баланс пополнен на {bonus_days} дней за пополнение вашего друга.</b>\n\n"
                                        "⚙️ <b>Для управления балансом перейдите в личный кабинет по кнопке в главном меню.</b>\n\n"
                                            "• Открыть главное меню: /start",
                                        parse_mode=ParseMode.HTML)


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
                            await self.bot.send_message(user.user_id,"⚠️ <b>На вашем балансе остался 1 день!</b>\n\nЕсли не пополнить баланс сейчас, то уже завтра VPN перестанет работать.\n\nПополнить баланс можно по кнопке ниже или в личном кабинете.",parse_mode=ParseMode.HTML,reply_markup=keyboard)
                            await self.app_manager.mark_notification_sent(user.user_id, 'day_before')
                        
                        elif remaining_days == 0 and not user.notify_day:
                            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="💸 Пополнить баланс",callback_data=NavConnect.TOPUP)]])
                            await self.bot.send_message(user.user_id,"⚠️ <b>На вашем балансе 0 дней, VPN больше не работает!</b>\n\nЧтобы VPN снова заработал, пополните баланс по кнопке ниже или в личном кабинете.",parse_mode=ParseMode.HTML,reply_markup=keyboard)
                            await self.app_manager.mark_notification_sent(user.user_id, 'day')

                        elif remaining_days <= -2 and user.notify_day_after == 0:
                            await self.app_manager.add_days_to_user(user.user_id, 5)
                            await self.bot.send_message(user.user_id,   "🎁 <b>Ваш баланс пополнен на 5 дней! Это единоразовая акция.</b>\n\n"
                                                                        "⚙️ <b>Для подключения VPN и управления балансом перейдите в личный кабинет по кнопке в главном меню.</b>\n\n" 
                                                                        "• Открыть главное меню: /start",
                                                                        parse_mode=ParseMode.HTML)
                            await self.app_manager.mark_notification_sent(user.user_id, 'day_after')
                    
                    except Exception as e:
                        print(f"Error sending notification to user {user.user_id}: {e}")
            
            except Exception as e:
                print(f"Notification checker error: {e}")
            
            await asyncio.sleep(60)

    async def total_notify(self):
        while True:
            users = await self.app_manager.get_users_for_notifications()
            current_time = time.time()
            for user in users:
                reg_time = user.registered_at.timestamp()
                expiry_seconds = user.expiry_time / 1000 if user.expiry_time > 1e12 else user.expiry_time
                remaining_days = ceil((expiry_seconds - current_time) / 86400)
                total = await self.app_manager.get_total(str(user.user_id))
                if total == 0 and user.notify_no_total == 0 and current_time - reg_time > 30:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⚙️ Подключить VPN", callback_data=NavConnect.INSTRUCTIONS)]])
                    await self.bot.send_message(
                            user.user_id,
                            "⚠️ <b>Вы еще не подключили VPN!</b>\n\n"
                            "Sosa VPN - это бесперебойная работа, до 5 устройств одновременно, стоимость меньше чашечки кофе!\n\n"
                            f"💸 <b>Ваш баланс: {remaining_days} дней</b>\n\n"
                            "⚙️ Подключите VPN, используя кнопку ниже или в личном кабинете по кнопке в главном меню.",
                            parse_mode=ParseMode.HTML,
                            reply_markup=keyboard
                        )
                    await self.app_manager.mark_notification_sent(user.user_id, 'no_total')
            await asyncio.sleep(5)



    async def start(self):
        asyncio.create_task(self.transaction_checker())
        asyncio.create_task(self.notification_checker())
        asyncio.create_task(self.total_notify())
        #asyncio.create_task(self.set_notifys())

        await self.dp.start_polling(self.bot)




