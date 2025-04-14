from modules.keys_db import Keys_DB
from modules.keys_notify_db import Keys_notify_DB
import asyncio
from configs.main_config import db_filename

class Key_origin():
    db_key = 0
    server_key = 1
    failed_key = 2

class received_key():
    succes = True
    failed = False
    def __init__(self,status,origin, key):
        self.success = status
        self.origin = origin
        self.key = key

class key_getter():
    def __init__(self):
        pass

    def get_key(self) -> received_key:
        key = self.get_from_server()
        if key.success:
            return key
        key = self.get_from_reserve_db()
        if key.success:
            return key
        key = received_key(received_key.failed,Key_origin.failed_key,None)
        return key

    def get_from_reserve_db(self) ->received_key:
        return received_key(received_key.succes,Key_origin.server_key,"key_1")

    def get_from_server(self) -> received_key:
        pass

class Keys_handler():
    def __init__(self):
        self.keys_db = Keys_DB(db_filename)
        self.keys_notify_db = Keys_notify_DB(db_filename)
        self.key_getter = key_getter()


    def get_key(self):
        return "key_1"

    async def start_keys_pending_polling(self):
        self.isRunning = True
        while self.isRunning:
            pending_keys = await self.keys_db.get_by_issued(False)
            for pending_key in pending_keys:
                key = self.key_getter.get_key()
                if key.succes:
                    uuid  = pending_key.uuid
                    await self.keys_db.issue_key(uuid,key)
                    await self.keys_notify_db.add_notification(uuid,)
            await asyncio.sleep(10)

    # async def start_keys_notifications_polling(self):
    #     self.isRunning = True
    #     while self.isRunning:
    #         pending_keys = await self.keys_db.get_by_issued(False)
    #         for pending_key in pending_keys:
    #             key = self.key_getter.get_key()
    #             if key.succes:
    #                 await self.keys_db.issue_key(pending_key.uuid,key)

    #         await asyncio.sleep(10)