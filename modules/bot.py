from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
import config


class vpnBot():
    def __init__(self):
        self.BOT_TOKEN = config.TELERAM_API_KEY
        self.bot = Bot(token=self.BOT_TOKEN)
        self.dp = Dispatcher()

    def init_keyboards():
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
            await register_user(message.from_user.id, ref)

            photo = FSInputFile("vpn_banner.jpg")
            welcome_caption = texts.welcome_text
            await message.answer_photo(photo=photo, caption=welcome_caption)
            await message.answer("Вы перенесены в главное меню.", reply_markup=main_keyboard)

        @self.dp.message(lambda message: message.text == "⚙️ Подключить VPN")
        async def handle_get_key(message: types.Message):
            photo = FSInputFile("vpn_banner.jpg")
            caption = (
                "⚡️ Вы покупаете премиум подписку на Sosa VPN.\n\n"
                "• До 5 устройств одновременно\n"
                "• Без ограничений по скорости и трафику"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                #[InlineKeyboardButton(text="7 дней — 50₽", callback_data="confirm_vpn_7")],
                [InlineKeyboardButton(text="1 месяц — 100₽", callback_data="confirm_vpn_30")]
            ])
            await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard)

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

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Подтвердить", callback_data=purchase_code)]
            ])
            await callback.message.answer(
                f"Вы собираетесь купить VPN на {days} дней.\n"
                f"С вашего баланса будет списано {cost}₽.",
                reply_markup=keyboard
            )

        @self.dp.callback_query(lambda c: c.data.startswith("vpn_"))
        async def handle_vpn_purchase(callback: types.CallbackQuery):
            user_id = callback.from_user.id
            if callback.data == "vpn_7":
                days = 7
                cost = 50
                key_file = "keys_7.txt"
            else:
                days = 30
                cost = 100
                key_file = "keys_30.txt"

            async with aiosqlite.connect("db.sqlite3") as db:
                user = await db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
                data = await user.fetchone()
                balance = data[0] if data else 0

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

                await db.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (cost, user_id))
                await db.commit()

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
            async with aiosqlite.connect("db.sqlite3") as db:
                user = await db.execute("SELECT balance, referrals FROM users WHERE user_id = ?", (user_id,))
                data = await user.fetchone()

            ref_link = f"https://t.me/{(await bot.get_me()).username}?start={user_id}"
            balance = data[0] if data else 0
            refs = data[1] if data else 0

            msg = (
                f"<b>👤 Профиль</b>\n"
                f"Баланс: {balance}₽\n"
                f"Приглашено: {refs} чел.\n\n"
                f"🔗 Твоя реферальная ссылка:\n{ref_link}"
            )
            await message.answer(msg, parse_mode=ParseMode.HTML)

        @self.dp.message(lambda message: message.text == "ℹ️ Информация")
        async def handle_info(message: types.Message):
            text = texts.info
            support_button = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✉️ Написать поддержке", url="https://t.me/nasralbek")]
            ])
            await message.answer(text, reply_markup=support_button)

    async def start(self):
        await self.dp.start_polling()
