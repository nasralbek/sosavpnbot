from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
import asyncio 

import configs.main_config as config
import modules.bot.texts as texts

from modules.yookassaAPI.yookassa_handler import Yookassa_handler

from modules.databases.DB_GINO_MANAGER import DatabaseManager
from modules.databases.enums.users_enum import RegisterUserEnum 

from modules.bot.keyboards import MainBoardKeyboards

class vpnBot():
    def __init__(self,db_manager:DatabaseManager):
        self.BOT_TOKEN = config.TELERAM_API_KEY
        self.bot = Bot(token=self.BOT_TOKEN)
        self.dp = Dispatcher()
        self.yookassa_handler = Yookassa_handler()
        self.keyboards = MainBoardKeyboards()
        self.db_manager = db_manager
        
        self.sosa_vpn_banner = FSInputFile("./src/vpn_banner.jpg")

    async def notify_register_by_ref(self,user_id,ref_id):
        #notify new user
        try:
            await self.bot.send_message(ref_id, texts.notify_referrer)
        except Exception as e:
            print(f"Ошибка при уведомлении пригласителя: {e}")
        #notify inviter
        try:
            await self.bot.send_message(user_id,texts.notify_invited)
        except Exception as e:
            print(f"Ошибка при уведомлении пользователя: {e}")

    def init_handlers(self):
        @self.dp.message(lambda message: message.text.startswith("/start"))
        async def handle_start(message: types.Message):
            #getting ids
            ref_id = message.text.split(" ")[1] if len(message.text.split()) > 1 else None
            user_id = message.from_user.id

            #register user
            register_status = await self.db_manager.register_user(user_id,ref_id)

            #answer 
            welcome_caption = texts.welcome_text
            await message.answer_photo(photo=self.sosa_vpn_banner,
                                       caption=welcome_caption,
                                       reply_markup=self.main_keyboard)

            #notify referral program
            if register_status == RegisterUserEnum.register_success:
                if not ref_id:
                    await self.notify_register_by_ref(user_id,ref_id)

            # await message.answer("Вы перенесены в главное меню.", reply_markup=self.main_keyboard)

        @self.dp.message(lambda message: message.text == "⚙️ Подключить VPN")
        async def handle_get_key(message: types.Message):
            
            caption = texts.connect_vpn_message
            
            await message.answer_photo(photo=self.sosa_vpn_banner, caption=caption, reply_markup=keyboard)

        @self.dp.callback_query(lambda c: c.data.startswith("select_vpn_"))
        async def handle_select_vpn(callback: types.CallbackQuery):
            match callback.data:
                case "select_vpn_30":
                    days = 30
                    cost = 100
                    purchase_code = "vpn_30"
                case "select_vpn_7":
                    days = 7
                    cost = 50
                    purchase_code = "vpn_7"    
            msg_text = "Выберите способо оплаты"
            
            # keyboard = InlineKeyboardMarkup(inline_keyboard=[
            #     [InlineKeyboardButton(text="Оплатить через yoomoney", callback_data="confirm_vpn_yoomoney_{days}")],
            #     [InlineKeyboardButton(text="Оплатить бонусами", callback_data="confirm_vpn_bonuses_{days}")]
            # ])
            keyboard = self.keyboards.purshare_method_keyboard(days)
            await callback.message.edit_caption(caption = msg_text,reply_markup=days)


        @self.dp.callback_query(lambda c: c.data.startswith("confirm_vpn_"))
        async def confirm_vpn(callback: types.CallbackQuery):
            if callback.data == "confirm_vpn_7":
                days = 7
                cost = 50
                purchase_code = "vpn_7"
            else:
                days = 30
                cost = 100
                purchase_code = "vpn_30"

            #print(callback)
            if "bonuses" in callback.data:
                msg_text =  texts.gen_want_to_purshare_balance(days,cost)
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Подтвердить", callback_data=purchase_code)]
                ])
            elif "yoomoney" in callback.data:
                url = await self.yookassa_handler.create_payment(callback.from_user.id,cost)
                msg_text =  texts.gen_want_to_purshare_yokassa(days,cost,url)
                keyboard = InlineKeyboardMarkup(inline_keyboard = [])
            await callback.message.edit_caption(caption = msg_text,reply_markup=keyboard)

        @self.dp.callback_query(lambda c: c.data.startswith("vpn_"))
        async def handle_vpn_purchase(callback: types.CallbackQuery):
            user_id = callback.from_user.id
            if callback.data == "vpn_7":
                days = 7
                cost = 50
                key_file = "../data/keys/keys_7.txt"
            else:
                days = 30
                cost = 100
                key_file = "../data/keys/keys_30.txt"
            
            
            if "balance" in callback.data:
                balance = await self.users_db.get_balance(user_id)
                if balance < cost:
                    await callback.message.answer(texts.not_enough_money_text)
                    return
                try:
                    with open(key_file, "r", encoding="utf-8") as f:
                        keys = f.readlines()
                except FileNotFoundError:
                    await callback.message.answer("❌ Файл с ключами не найден.")
                    return
                if not keys:
                    await callback.message.answer("❌ Ключи закончились.")
                    return

            key = keys[0].strip()
            with open(key_file, "w", encoding="utf-8") as f:
                f.writelines(keys[1:])

            await self.users_db.increase_balance(user_id,-cost)

            await callback.message.answer(
                f"🔑 Твой VPN-ключ на {days} дней:\n\n<code>{key}</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=self.keyboards.instrucion_keyboard
            )

        @self.dp.callback_query(lambda c: c.data.startswith("how_"))
        async def handle_instructions(callback: types.CallbackQuery):
            data = callback.data
            if data == "how_ios":
                text = texts.how_ios
            elif data == "how_android":
                text = texts.how_android
            elif data == "how_windows":
                text = texts.how_windows
            elif data == "how_macos":
                text = texts.how_macos
            else:
                text = texts.how_not_found

            await callback.message.answer(text, parse_mode=ParseMode.HTML)


        @self.dp.message(lambda message: message.text == "🏠 Профиль")
        async def handle_profile(message: types.Message):
            user_id  = message.from_user.id
            ref_link = texts.gen_reflink((await self.bot.get_me()).username,user_id)
            balance  = await self.users_db.get_balance(user_id)
            refs     = await self.users_db.get_refs(user_id)
            
            msg = texts.profile_text(balance,refs,ref_link)
            
            await message.answer(msg, parse_mode=ParseMode.HTML)

        @self.dp.message(lambda message: message.text == "ℹ️ Информация")
        async def handle_info(message: types.Message):
            text = texts.info
            support_button = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✉️ Написать поддержке", url="https://t.me/nasralbek")]
            ])
            await message.message.answer(text, reply_markup=support_button)

    async def start_polling_pending_notifications(self):
        while True:
            try:
                pending_notifies = await self.keys_notify_db.get_by_notified(notified_status = False)
                for pending_notification in pending_notifies:
                    uuid = pending_notification.uuid_in_keys
                    key = await self.keys_db.get_key(uuid)
                    user_id = await self.keys_db.get_user_id(uuid)
                    #print(key,user_id)
                    try:
                        await self.bot.send_message(chat_id = user_id,text = f"ваш ключ: \n{key}")
                        await self.keys_notify_db.set_notified(uuid)

                    except Exception as e:
                        print(e)

                
            except Exception as e:
                print(e)
            await asyncio.sleep(1)

    async def start(self):
        # depreceated
        # yookassa_task = asyncio.create_task(self.yookassa_handler.start_check_payments())
        # keys_task = asyncio.create_task(self.keys_handler.start_keys_pending_polling())
        # notifies_task = asyncio.create_task(self.start_polling_pending_notifications())
        await self.dp.start_polling(self.bot)
