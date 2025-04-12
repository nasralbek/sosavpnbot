import asyncio
import aiosqlite
class DB():
    def __init__(self,filename):
        self.db_name = filename

    

    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        balance INTEGER DEFAULT 0,
                        invited_by INTEGER,
                        referrals INTEGER DEFAULT 0
                    )
                """)
                await db.commit()
        except Exception as e:
            self.connection_failed(e)

    async def register_user(self,user_id, ref=None):
        try: 
            async with aiosqlite.connect(self.db_name ) as db:
                print(db)
                user = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                result = await user.fetchone()
                if result is None:
                    if ref and int(ref) != user_id:
                        #await db.execute("INSERT INTO users (user_id, balance, invited_by) VALUES (?, ?, ?)", (user_id, 100, ref))
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
        except Exception as e:
            self.connection_failed(e)



    async def get_balance(self,user_id):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                balance_sql = await db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
                data = await balance_sql.fetchone()
                balance = data[0] if data else 0
                return balance
        except Exception as e:
            self.connection_failed(e)
            
    async def get_refs(self,user_id):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                refs_sql = await db.execute("SELECT referrals FROM users WHERE user_id = ?", (user_id,))
                data = await refs_sql.fetchone()
                refs = data[0] if data else 0
                return refs
        except Exception as e:
            self.connection_failed(e)

    async def update_balance(self,user_id,new_balance):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                await db.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
                await db.commit()
        except Exception as e:
            self.connection_failed(e)

    async def write_off_balance(self,user_id,cost):
        current_balance = await self.get_balance(user_id)
        new_balance = current_balance - cost
        await self.update_balance(user_id,new_balance)
            

    def  connection_failed(self,e):
        print(f"failed to connect db: {e}")

    async def start(self):
        await self.init_db()