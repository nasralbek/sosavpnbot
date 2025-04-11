import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

BOT_TOKEN = '7518561707:AAGhfU3wyVR2Sf30u3Sk1e2Mxteb8UbBI-k'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='⚙️ Подключить VPN')],
        [KeyboardButton(text='🏠 Профиль'), KeyboardButton(text='ℹ️ Информация')]
    ],
    resize_keyboard=True
)

async def init_db():
    async with aiosqlite.connect('db.sqlite3') as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                invited_by INTEGER,
                referrals INTEGER DEFAULT 0
            )
        """)
        await db.commit()

async def register_user(user_id, ref=None):
    async with aiosqlite.connect('db.sqlite3') as db:
        user = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        result = await user.fetchone()

        if result is None:
            if ref and int(ref) != user_id:
                await db.execute("INSERT INTO users (user_id, balance, invited_by) VALUES (?, ?, ?)", (user_id, 100, ref))
                await db.execute("UPDATE users SET balance = balance + 50, referrals = referrals + 1 WHERE user_id = ?", (ref,))
                await db.commit()

                try:
                    await bot.send_message(ref, "🎉 Новый пользователь зарегистрировался по твоей ссылке! Тебе начислено 50₽.")
                except Exception as e:
                    print(f"Ошибка при уведомлении пригласителя: {e}")

                try:
                    await bot.send_message(user_id, "🎁 Добро пожаловать! Тебе начислено 100₽ за регистрацию по реферальной ссылке.")
                except Exception as e:
                    print(f"Ошибка при уведомлении пользователя: {e}")
            else:
                await db.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, 0))
                await db.commit()

@dp.message(lambda message: message.text.startswith("/start"))
async def handle_start(message: types.Message):
    ref = message.text.split(" ")[1] if len(message.text.split()) > 1 else None
    await register_user(message.from_user.id, ref)

    photo = FSInputFile("vpn_banner.jpg")
    welcome_caption = (
        "Я Ваш личный бот и помощник Sosa VPN!\n\n"
        "Я помогаю c обходом блокировок и защитой вашей конфиденциальности.\n\n"
        "Для использования сервиса Вам не нужно нигде регистрироваться, просто оплатите подписку и начните пользоваться VPN.\n"
        "Все происходит внутри Telegram."
    )
    await message.answer_photo(photo=photo, caption=welcome_caption)
    await message.answer("Вы перенесены в главное меню.", reply_markup=main_keyboard)

@dp.message(lambda message: message.text == "⚙️ Подключить VPN")
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

@dp.callback_query(lambda c: c.data.startswith("confirm_vpn_"))
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

@dp.callback_query(lambda c: c.data.startswith("vpn_"))
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

@dp.callback_query(lambda c: c.data.startswith("how_"))
async def handle_instructions(callback: types.CallbackQuery):
    data = callback.data
    if data == "how_ios":
        text = (
            "📱 <b>Инструкция для iOS</b>:\n"
            "1. Установи Hiddify из App Store.\n"
            "2. Открой приложение и нажми “+”.\n"
            "3. Выбери “Импорт из текста”.\n"
            "4. Вставь ключ и нажми “Сохранить”.\n"
            "5. Нажми “Подключиться”."
        )
    elif data == "how_android":
        text = (
            "🤖 <b>Инструкция для Android</b>:\n"
            "1. Установи Hiddify из Google Play или с сайта hiddify.com.\n"
            "2. Открой приложение и нажми “+”.\n"
            "3. Выбери “Импорт из текста”.\n"
            "4. Вставь ключ и нажми “Сохранить”.\n"
            "5. Нажми “Старт” для подключения."
        )
    elif data == "how_windows":
        text = (
            "🪟 <b>Инструкция для Windows</b>:\n"
            "1. Скачай Hiddify с сайта hiddify.com.\n"
            "2. Установи и открой программу.\n"
            "3. Нажми “Импорт → Из текста”.\n"
            "4. Вставь ключ и нажми “Импортировать”.\n"
            "5. Нажми “Подключиться”."
        )
    elif data == "how_macos":
        text = (
            "💻 <b>Инструкция для MacOS</b>:\n"
            "1. Установи Hiddify с сайта hiddify.com.\n"
            "2. Открой и нажми “+”.\n"
            "3. Выбери “Импорт из текста”.\n"
            "4. Вставь ключ и нажми “Добавить”.\n"
            "5. Нажми “Старт” для подключения."
        )
    else:
        text = "❗ Инструкция не найдена."

    await callback.message.answer(text, parse_mode=ParseMode.HTML)

@dp.message(lambda message: message.text == "🏠 Профиль")
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

@dp.message(lambda message: message.text == "ℹ️ Информация")
async def handle_info(message: types.Message):
    text = (
        "Sosa VPN использует протокол с открытым исходным кодом, который имеет наилучшую производительность, "
        "по сравнению с другими. Все наши сервера оснащены каналом 1 гбит/с.\n\n"
        "Журнал логов удаляется с наших серверов моментально, мы не храним историю посещений, в отличии от многих "
        "бесплатных сервисов. Мы не собираем и не продаём какие либо данные о Вас.\n\n"
        "Для выдачи доступа к VPN используется Telegram, в связи с этим нас не возможно заблокировать или удалить "
        "из App Store и других площадок."
    )
    support_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✉️ Написать поддержке", url="https://t.me/nasralbek")]
    ])
    await message.answer(text, reply_markup=support_button)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
