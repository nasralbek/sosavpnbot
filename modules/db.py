import asyncio
import aiosqlite

class DB():
    def __init__(self):
        pass

    
    def connect(self):
        try:
            self.db = aiosqlite.connect('db.sqlite3')
        except Exception as e:
            print(f"error while connecting database: {e}")

    async def init_db(self):
        async with aiosqlite.connect("db.sqlite3") as db:
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
        db=self.db
        user = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        result = await user.fetchone()
        async with aiosqlite.connect("db.sqlite3") as db:
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

    async def start(self):
        #self.connect()
        await self.init_db()