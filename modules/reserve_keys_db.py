import configs.SQL_queries.SQL_RESERVE_KEYS_QUERIES as SQLs
from modules.base_db import BaseDB
import aiosqlite

class Reserve_keys_DB(BaseDB):
    def __init__(self,filename):
        self.db_name = filename

        self.init_command = SQLs.create_reserve_keys_table
    async def get_key(self, notified_status = False):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.get_key)
                fetch = await execute_result.fetchone()
                key = fetch[0]
                execute_result2 = await db.execute(SQLs.issue_key,(key,))
                await db.commit()
                return key
        except Exception as e:
            print("there 1 0 ")
            self.connection_failed(e)

    async def add_key(self,key):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                execute_result = await db.execute(SQLs.add_key,(key))
                await db.commit()
        except Exception as e:
            self.connection_failed(e)
    async def add_keys(self,keys):
        for key in keys:
            await self.add_key(key)        