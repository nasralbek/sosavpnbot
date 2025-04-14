import configs.SQL_queries.SQL_KEY_NOTIFICACTIONS_QUERIES as SQLs
import aiosqlite
from modules.base_db import BaseDB


class notify_instance():
    def __init__(self,list,notified):
        self.uuid_in_keys = list[0]
        self.notified = notified

class Keys_notify_DB(BaseDB):
    def __init__(self,filename):
        self.db_name = filename

        self.init_command = SQLs.create_keys_notifications_table
    async def add_notification(self,uuid,notified = False):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.add_notification,(uuid,notified,))
                await db.commit()
        except Exception as e:
            self.connection_failed(e)

    async def get_by_notified(self,notified_status = False):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                execute_result = await db.execute(SQLs.get_by_notified,(notified_status,))
                result = await execute_result.fetchall()
                result = list(map(lambda x: notify_instance(x,notified_status),result))
                return result
        except Exception as e:
            self.connection_failed(e)
            return []
        
    async def set_notified(self,uuid,notified_status = True):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                execute_result = await db.execute(SQLs.set_notified,(notified_status,uuid))
                await db.commit()
        except Exception as e:
            self.connection_failed(e)