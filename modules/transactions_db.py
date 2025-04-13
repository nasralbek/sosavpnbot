import configs.SQL_queries.SQL_TRANSACTION_QUERIES as SQLs
from modules.base_db import BaseDB
import aiosqlite

class Transaction_status():
    success = 1    
    waiting = 2
    canceled = 3

    success_str = "success"
    waiting_str = "waiting"
    canceled_str = "canceled"

    def get_status_str(status: int) -> str:
        match status:
            case Transaction_status.success:return Transaction_status.success_str
            case Transaction_status.waiting:return Transaction_status.waiting_str
            case Transaction_status.canceled:return Transaction_status.canceled_str

    def get_status_code(status: str)-> int:
        match status:
            case Transaction_status.success_str:return Transaction_status.success
            case Transaction_status.waiting_str:return Transaction_status.waiting
            case Transaction_status.canceled_str:return Transaction_status.canceled

class Transactions_DB(BaseDB):
    def __init__(self,filename):
        self.db_name = filename
        self.init_command = SQLs.create_transactions_table
    
    async def create_transaction(self,
                                 user_id,
                                 amount,
                                 uuid,
                                 payment_id,
                                 status=Transaction_status.waiting
                                 ):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.insert_transaction,
                                                   (user_id,
                                                    amount,
                                                    Transaction_status.get_status_str(status),
                                                    uuid,payment_id))
                await db.commit()
        except Exception as e:
            self.connection_failed(e)

    async def set_transaction_status(self,uuid,status):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.set_status,
                                                   (Transaction_status.get_status_str(status),
                                                    uuid))
                await db.commit()
        except Exception as e:
            self.connection_failed(e)

    async def get_transaction_status(self,uuid):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.get_status,(uuid))
                return Transaction_status.get_status_code(execute_result)
        except Exception as e:
            self.connection_failed(e)
    async def get_payment_id(self,uuid):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.get_payment_id,(uuid,))
                result = await execute_result.fetchone()
                return result[0]
        except Exception as e:
            self.connection_failed(e)

    async def get_waiting_transactions(self):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.get_waiting_transactions)
                waiting_list = list(await execute_result.fetchall())
                waiting_list = list(map(lambda x: x[0],waiting_list))

                return waiting_list
        except Exception as e:
            
            self.connection_failed(e)
            return []

    async def set_key_requested(self,uuid,isRequested= True):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.set_key_requested, (isRequested,uuid))
                
        except Exception as e:
            self.connection_failed(e)

    async def get_user_id(self,uuid):
        try:
            async with aiosqlite.connect(self.db_name ) as db:
                execute_result = await db.execute(SQLs.get_user_id,(uuid,))
                result = await execute_result.fetchone()
                return (result[0])
        except Exception as e:
            self.connection_failed(e)