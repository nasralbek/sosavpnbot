from modules.databases.keys_db import Keys_DB
from modules.databases.keys_notify_db import Keys_notify_DB
from modules.databases.reserve_keys_db import Reserve_keys_DB
from configs.main_config import db_filename
from modules.xuiAPI.xuiAPI import X_UI_API
import asyncio

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
        self.x_ui_api = X_UI_API()


    async def get_key(self,uuid,user_id) -> received_key:
        key = await self.get_from_server(uuid,user_id)
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

    async def get_from_server(self,uuid,user_id) -> received_key:
        new_key = await self.x_ui_api.get_key(uuid,user_id)
        return received_key(received_key.success,Key_origin.server_key,new_key)

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
                    uuid  = pending_key.uuid
                    user_id = pending_key.user_id
                    key = await self.key_getter.get_key(uuid,user_id)
                    print(key)
                    if key.success_status:
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