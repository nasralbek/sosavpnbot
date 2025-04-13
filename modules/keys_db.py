from modules.base_db import BaseDB


class KeysDB(BaseDB):
    def __init__(self,filename):
        self.db_name = filename
        #self.init_command = SQLs.create_transactions_table
        self.init_command = """"""
    async def add_key(self,user_id):
        print(f"прошла оплато от :{user_id}") 
