from gino import Gino
from sqlalchemy import exists

from configs.main_config import PG_CONFIG

from modules.database.models.User_model import create_user_model
from modules.database.models.Transaction_model import create_transaction_model
import uuid
reg_by_ref_bonus = 100
invite_user_bonus = 50

class DatabaseManager():
    def __init__(self,db : Gino):
        self.db = db

        self.User = create_user_model(self.db)
        self.Transaction = create_transaction_model(self.db)
        
    async def init_tables(self):
        await self.db.gino.create_all()

    @classmethod
    async def auth(cls, host: str, port:str,dbname:str,login:str,password:str) -> 'DatabaseManager':
        db = Gino()
        uri = "postgresql://%s:%s@%s:%s/%s"  %  (login,    
                                                password,
                                                host,
                                                port,
                                                dbname)
        await db.set_bind(bind = uri)
        return cls(db)
    
    async def connect(self):
        if self.db_uri == None:
            raise Exception("db_uri not setted, \nyou need to set it with auth method")
        await self.db.connect(self.db_uri)
    
    async def auth_from_config():
        return await DatabaseManager.auth(PG_CONFIG.PG_HOST,
                             PG_CONFIG.PG_PORT,
                             PG_CONFIG.PG_DB_NAME,
                             PG_CONFIG.PG_USERNAME,
                             PG_CONFIG.PG_PASSWORD)
