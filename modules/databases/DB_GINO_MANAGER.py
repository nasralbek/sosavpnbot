from gino import Gino
from sqlalchemy import exists

from configs.main_config import PG_CONFIG

from modules.databases.models.User_model import create_user_model
from modules.databases.models.Key_model import create_key_model
from modules.databases.models.Key_parameters_model import create_key_parameters_model
from modules.databases.models.Transaction_model import create_transaction_model

from modules.databases.enums.users_enum import RegisterUserEnum
import uuid
reg_by_ref_bonus = 100
invite_user_bonus = 50

class DatabaseManager():
    def __init__(self,db : Gino):
        self.db = db

        self.User = create_user_model(self.db)
        self.Key = create_key_model(self.db)
        self.Key_paramaters = create_key_parameters_model(self.db)
        self.Transaction = create_transaction_model(self.db)
        
    async def init_tables(self):
        await self.db.gino.create_all()

    async def auth(host: str, port:str,dbname:str,login:str,password:str):
        db = Gino()
        uri = "postgresql://%s:%s@%s:%s/%s"  %  (login,    
                                                password,
                                                host,
                                                port,
                                                dbname)
        await db.set_bind(bind = uri)
        return DatabaseManager(db)
    
    async def auth_from_config():
        return await DatabaseManager.auth(PG_CONFIG.PG_HOST,
                             PG_CONFIG.PG_PORT,
                             PG_CONFIG.PG_DB_NAME,
                             PG_CONFIG.PG_USERNAME,
                             PG_CONFIG.PG_PASSWORD)
    async def lirili_larila(self,user_id,days):
        user = self.get_user(user_id)
        user.lirili_larila(days)


    async def connect(self):
        if self.db_uri == None:
            raise Exception("db_uri not setted, \nyou need to set it with auth method")
        await self.db.connect(self.db_uri)

    async def register_user(self,user_id,uuid,sub_id,expiry_time):
        if await self.is_user_exists(user_id):
            return RegisterUserEnum.user_already_exists
        new_user = await self.User.create(  user_id    = user_id     ,
                                            uuid        = uuid       ,
                                            sub_id      = sub_id     ,
                                            expiry_time = expiry_time   )
        return RegisterUserEnum.register_success

    async def add_referral(self,user_id,referral_id):
        try:
            invited_user  = await self.get_user(user_id)  
            referral_user = await self.get_user(referral_id)
            await invited_user.set_referral(referral_id)
            await referral_user.increase_referrals(1)
        except Exception as e:
            print(e)

    async def create_key(self,user_id,key_uuid):
        await self.Key.create(user_id = user_id,key_uuid = key_uuid)
        await self.Key_paramaters.create(user_id = user_id,key_uuid = key_uuid)

    async def get_user(self,user_id):
        user =  await self.User.query.where(self.User.user_id == user_id ).gino.one()
        return user
        
    async def get_balance(self,user_id):
        user = await self.get_user(user_id)
        return user.balance
    
    async def get_key(self,user_id):
        key = await self.Key.query.where(self.Key.user_id == user_id ).gino.one()
        return key.string()
    
    async def get_referrals(self,user_id):
        user = await self.get_user(user_id)
        return user.referrals

    async def is_user_exists(self,user_id) -> bool:
        result = await self.db.scalar(exists().where(self.User.user_id == user_id).select())
        return result
