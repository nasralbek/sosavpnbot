import aiosqlite

class BaseDB():
    def __init__(self):
        self.init_command = ''''''
        
    def  connection_failed(self,e):
        print(f"failed to connect db: {e}")

    async def start(self):
        await self.init_db()

    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                await db.execute(self.init_command)
                await db.commit()
        except Exception as e:
            self.connection_failed(e)