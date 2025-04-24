from gino import Gino
from sqlalchemy import exists

from modules.databases.gino.models.User_model import create_user_model
from modules.databases.gino.models.Key_model import create_key_model
from modules.databases.gino.models.Key_parameters_model import create_key_parameters_model
from modules.databases.gino.models.Transaction_model import create_transaction_model

from modules.databases.gino.enums.users_enum import RegisterUserEnum
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

    async def connect(self):
        if self.db_uri == None:
            raise Exception("db_uri not setted, \nyou need to set it with auth method")
        await self.db.connect(self.db_uri)

    async def register_user(self,user_id,refferral_id=None):
        if await self.is_user_exists(user_id):
            return RegisterUserEnum.user_already_exists
        key_uuid = uuid.uuid4()
        new_user = await self.User.create(user_id = user_id,invited_by = refferral_id,key_uuid = key_uuid)
        if refferral_id:
            referral_user = await self.get_user(refferral_id)
            await new_user.increase_balance(reg_by_ref_bonus)
            await referral_user.increase_balance(invite_user_bonus)
            await referral_user.increase_referrals(1)
        await self.create_key(user_id,new_user.key_uuid)
        return RegisterUserEnum.register_success

    async def create_key(self,user_id,key_uuid):
        await self.Key.create(user_id = user_id,key_uuid = key_uuid)
        await self.Key_paramaters.create(user_id = user_id,key_uuid = key_uuid)

    async def get_user(self,user_id):
        return await self.User.query.where(self.User.user_id == user_id ).gino.one()
        
    async def is_user_exists(self,user_id) -> bool:
        result = await self.db.scalar(exists().where(self.User.user_id == user_id).select())
        return result
