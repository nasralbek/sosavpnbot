from modules.databases.base_db import BaseDB
import configs.SQL_queries.SQL_KEYS_QUERIES as SQLs
import aiosqlite
from uuid import uuid4

class issue_instance():
    def __init__(self,list,isIssued):
        self.user_id = list[0]
        self.uuid = list[1]
        self.isIssued = isIssued


class Keys_DB(BaseDB):
    def __init__(self,filename):
        self.db_name = filename

        self.init_command = SQLs.create_keys_table
    async def add_pending(self,user_id):
        try:
            uuid = str(uuid4())
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.add_pending,
                                                   (user_id,
                                                    False,
                                                    uuid
                                                    )
                                                )
                await db.commit()
        except Exception as e:
            self.connection_failed(e)

    async def get_by_issued(self,issued_status = False):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.select_by_issued,(issued_status,))
                result = await execute_result.fetchall()
                result = list(map(lambda x: issue_instance(x,issued_status),result))
                return result
        except Exception as e:
            self.connection_failed(e)
            return []
        
    async def issue_key(self,uuid,key):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                execute_result = await db.execute(SQLs.issue_key,(key,True,uuid))
                await db.commit()
        except Exception as e:
            print("there")
            self.connection_failed(e)
            return []

    async def get_key(self,uuid):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.get_key,(uuid,))
                result = await execute_result.fetchone()
                result = list(result)[0]
                return result
        except Exception as e:
            self.connection_failed(e)
            return []


    async def get_user_id(self,uuid):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.get_user_id,(uuid,))
                result = await execute_result.fetchone()
                result = list(result)[0]
                return result
        except Exception as e:
            self.connection_failed(e)
            return []