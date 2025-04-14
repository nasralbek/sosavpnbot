from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
import asyncio 
import configs.main_config as config
import configs.texts.texts as texts
from modules.yookassa_handler import Yookassa_handler
from modules.keys_handler import Keys_handler
from modules.keys_notify_db import Keys_notify_DB
from modules.keys_db import Keys_DB


class vpnBot():
    def __init__(self,db):
        self.BOT_TOKEN = config.TELERAM_API_KEY
        self.bot = Bot(token=self.BOT_TOKEN)
        self.dp = Dispatcher()
        self.yookassa_handler = Yookassa_handler()
        self.keys_handler=  Keys_handler()
        self.init_keyboards()
        self.init_handlers()
        self.users_db = db
        self.keys_notify_db = Keys_notify_DB(config.db_filename)
        self.keys_db = Keys_DB(config.db_filename)
        self.sosa_vpn_banner = FSInputFile("./src/vpn_banner.jpg")


    def init_keyboards(self):
        self.main_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='⚙️ Подключить VPN')],
                [KeyboardButton(text='🏠 Профиль'), KeyboardButton(text='ℹ️ Информация')]
            ],
            resize_keyboard=True
        )

    def init_handlers(self):
        @self.dp.message(lambda message: message.text.startswith("/start"))
        async def handle_start(message: types.Message):
            ref = message.text.split(" ")[1] if len(message.text.split()) > 1 else None
            user_id = message.from_user.id
            register_status = await self.users_db.register_user(user_id, ref)


            welcome_caption = texts.welcome_text
            await message.answer_photo(photo=self.sosa_vpn_banner, caption=welcome_caption,reply_markup=self.main_keyboard)

            if register_status.ok():
                if not (register_status.refferal is None):
                    try:
                        await self.bot.send_message(ref, "🎉 Новый пользователь зарегистрировался по твоей ссылке! Тебе начислено 50₽.")
                    except Exception as e:
                        print(f"Ошибка при уведомлении пригласителя: {e}")
                    try:
                        await self.bot.send_message(user_id, "🎁 Добро пожаловать! Тебе начислено 100₽ за регистрацию по реферальной ссылке.")
                    except Exception as e:
                        print(f"Ошибка при уведомлении пользователя: {e}")

            # await message.answer("Вы перенесены в главное меню.", reply_markup=self.main_keyboard)

        @self.dp.message(lambda message: message.text == "⚙️ Подключить VPN")
        async def handle_get_key(message: types.Message):
            
            caption = (
                "⚡️ Вы покупаете премиум подписку на Sosa VPN.\n\n"
                "• До 5 устройств одновременно\n"
                "• Без ограничений по скорости и трафику"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                #[InlineKeyboardButton(text="7 дней — 50₽", callback_data="confirm_vpn_7")],
                [InlineKeyboardButton(text="1 месяц — 100₽", callback_data="select_vpn_30")]
            ])
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
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Оплатить через yoomoney", callback_data="confirm_vpn_yoomoney_{days}")],
                [InlineKeyboardButton(text="Оплатить бонусами", callback_data="confirm_vpn_bonuses_{days}")]
            ])
            await callback.message.edit_caption(caption = msg_text,reply_markup=keyboard)


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
                msg_text =  f"Вы собираетесь купить VPN на {days} дней.\n"\
                            f"С вашего баланса будет списано {cost}₽."
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Подтвердить", callback_data=purchase_code)]
                ])
            elif "yoomoney" in callback.data:
                url = await self.yookassa_handler.create_payment(callback.from_user.id,cost)
                msg_text =  f"Стоимость: {cost}\n" \
                            f"Ссылка для оплаты vpn:\n"\
                            f"{url}"
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
                    await callback.message.answer("❌ Недостаточно средств на балансе.")
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

            instruction_buttons = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📱 iOS", callback_data="how_ios"),
                InlineKeyboardButton(text="🤖 Android", callback_data="how_android")],
                [InlineKeyboardButton(text="🪟 Windows", callback_data="how_windows"),
                InlineKeyboardButton(text="💻 MacOS", callback_data="how_macos")]
            ])

            await callback.message.answer(
                f"🔑 Твой VPN-ключ на {days} дней:\n\n<code>{key}</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=instruction_buttons
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
                text = "❗ Инструкция не найдена."

            await callback.message.answer(text, parse_mode=ParseMode.HTML)

        @self.dp.message(lambda message: message.text == "🏠 Профиль")
        async def handle_profile(message: types.Message):
            user_id = message.from_user.id
            ref_link = f"https://t.me/{(await self.bot.get_me()).username}?start={user_id}"
            balance = await self.users_db.get_balance(user_id)
            refs = await self.users_db.get_refs(user_id)
            msg = (
                f"Баланс: <b>{balance}</b>₽\n"
                f"Приглашено: <b>{refs} чел.</b>\n\n"
                f"🔗 За каждого приглашенного друга ты получаешь 50₽ на баланс, друг получает 100₽.\n\n"
                f"👥 <b>Твоя реферальная ссылка:</b>\n{ref_link}\n"
            )
            await message.answer(msg, parse_mode=ParseMode.HTML)

        @self.dp.message(lambda message: message.text == "ℹ️ Информация")
        async def handle_info(message: types.Message):
            text = texts.info
            support_button = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✉️ Написать поддержке", url="https://t.me/nasralbek")]
            ])
            await message.answer(text, reply_markup=support_button)

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
        yookassa_task = asyncio.create_task(self.yookassa_handler.start_check_payments())
        keys_task = asyncio.create_task(self.keys_handler.start_keys_pending_polling())
        notifies_task = asyncio.create_task(self.start_polling_pending_notifications())
        await self.dp.start_polling(self.bot)
