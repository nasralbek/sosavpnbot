from modules.databases.keys_db import Keys_DB
from modules.databases.keys_notify_db import Keys_notify_DB
from modules.databases.reserve_keys_db import Reserve_keys_DB
import asyncio
from configs.main_config import db_filename


class Key_origin():
    server_key = 0
    reserve_db_key = 1
    failed_key = 2

class received_key():
    success = True
    failed = False
    def __init__(self,status,origin, key):
        self.success_status = status
        self.origin = origin
        self.key = key
        

class key_getter():
    def __init__(self):
        self.reserve_keys_db = Reserve_keys_DB(db_filename)

    async def get_key(self) -> received_key:
        print("getting")
        key = self.get_from_server()
        print("getted")
        if key.success_status:
            print("returned")
            return key
        key = await self.get_from_reserve_db()
        if key.success_status:
            print("returned_db")
            return key
        key = received_key(received_key.failed,Key_origin.failed_key,None)
        return key

    async def get_from_reserve_db(self) ->received_key:
        return received_key(received_key.success,Key_origin.reserve_db_key,await self.reserve_keys_db.get_key())

    def get_from_server(self) -> received_key:
        return received_key(received_key.failed,Key_origin.server_key,"key_1")

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
                try:
                    key =await  self.key_getter.get_key()
                    print(key)
                    if key.success_status:
                        uuid  = pending_key.uuid
                        await self.keys_db.issue_key(uuid,key.key)
                        await self.keys_notify_db.add_notification(uuid,)
                except Exception as e:
                    print(e)
            
            await asyncio.sleep(1)

    # async def start_keys_notifications_polling(self):
    #     self.isRunning = True
    #     while self.isRunning:
    #         pending_keys = await self.keys_db.get_by_issued(False)
    #         for pending_key in pending_keys:
    #             key = self.key_getter.get_key()
    #             if key.succes:
    #                 await self.keys_db.issue_key(pending_key.uuid,key)

    #         await asyncio.sleep(10)