import asyncio
import aiosqlite
import configs.SQL_queries.SQLs as SQLs
from modules.base_db import BaseDB

#TODO: move this to other file
class Register_user_status():
    def __init__(self):
        self.refferal = None
        self.register_ok = False

    def ok(self):return self.register_ok

class Users_DB(BaseDB):
    def __init__(self,filename):
        self.db_name = filename
        self.init_command = SQLs.create_users_table


    async def register_user(self,user_id, ref=None) -> Register_user_status:
        status = Register_user_status()
        try: 
            async with aiosqlite.connect(self.db_name ) as db:
                user = await db.execute(SQLs.select_user_from_users, (user_id,))
                result = await user.fetchone()
                if result is None:
                    if ref and int(ref) != user_id:
                        status.refferal = ref
                        await self.add_user(user_id,100,ref)
                        await self.add_referal(ref)
                        await self.increase_balance(ref,50)
                        status.register_ok = True
                    else:
                        await self.add_user(user_id,0,None)
                        status.register_ok = True
        except Exception as e:
            self.connection_failed(e)
        finally:
            return status



    async def add_user(self,user_id,balance,invited_by,referrals = 0):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                balance_sql = await db.execute(SQLs.insert_new_user, (user_id,balance,invited_by,referrals))
                await db.commit()
        except Exception as e:
            self.connection_failed(e)

    async def get_balance(self,user_id):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                balance_sql = await db.execute(SQLs.select_balance_from_users, (user_id,))
                data = await balance_sql.fetchone()
                balance = data[0] if data else 0
                return balance
        except Exception as e:
            self.connection_failed(e)
            
    async def get_refs(self,user_id):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                refs_sql = await db.execute(SQLs.select_referals_from_users, (user_id,))
                data = await refs_sql.fetchone()
                refs = data[0] if data else 0
                return refs
        except Exception as e:
            self.connection_failed(e)

    async def update_balance(self,user_id,new_balance):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                await db.execute(SQLs.update_user_balance, (new_balance, user_id))
                await db.commit()
        except Exception as e:
            self.connection_failed(e)

    async def increase_balance(self,user_id,count):
        current_balance = await self.get_balance(user_id)
        new_balance = current_balance + count
        await self.update_balance(user_id,new_balance)
            
    async def update_referals(self,user_id,new_referrals):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                await db.execute(SQLs.update_user_referals, (new_referrals, user_id))
                await db.commit()
        except Exception as e:
            self.connection_failed(e)

    async def add_referal(self,user_id):
        current_refs = await self.get_refs(user_id)
        new_referrals = current_refs+1
        await self.update_referals(user_id,new_referrals)

