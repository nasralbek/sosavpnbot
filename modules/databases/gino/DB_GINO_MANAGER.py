from gino import Gino
from modules.databases.gino.models.User_model import create_user_model
from modules.databases.gino.models.Key_model import create_key_model

from modules.databases.gino.enums.users_enum import RegisterUserEnum

reg_by_ref_bonus = 150
invite_user_bonus = 75

class DatabaseManager():
    def __init__(self,db : Gino,db_uri:str):
        self.db = db
        self.db_uri

        self.User = create_user_model(self.db)

    def auth(self,host: str, port:str,dbname:str,login:str,password:str):
        self.db_uri = "postgresql://%s:%s/%s:%s/%s"  %  (login,    
                                                        password,
                                                        host,
                                                        port,
                                                        dbname)

    async def connect(self):
        if self.db_uri == None:
            raise Exception("db_uri not setted, \nyou need to set it with auth method")
        await self.db.connect(self.db_uri)

    async def init_tables(self):
        self.db.gino.create_all()

    async def register_user(self,user_id,refferral_id=None):
        if await self.is_user_exists(user_id):
            return RegisterUserEnum.user_already_exists
        new_user = await self.User.Create(user_id = user_id,invited_by = refferral_id)
        if refferral_id:
            referral_user = await self.get_user(refferral_id)
            await referral_user.update(referrals = referral_user.referrals+1)
            await self.increase_balance(user_id,reg_by_ref_bonus)
            await self.increase_balance(refferral_id,)
        self.create_key()

    async def create_key(self,user_id):
        await self.Key.Create(user_id = user_id)


    async def get_user(self,user_id):
        return await self.User.query.where(self.User.user_id == user_id ).gino.one()
        
    async def set_user_balance(self,user_id,new_balance):
        user = await self.get_user(user_id)
        user.update(balance = new_balance)
    
    async def increase_balance(self,user_id,increase_amount):
        user = await self.get_user(user_id)
        await user.update(balance = user.balance+increase_amount)

    async def decrease_balance(self,user_id,decrease_amount):
        await self.increase_balance(user_id,-decrease_amount)

    async def is_user_exists(self,user_id) -> bool:
        result = await self.User.query.where(self.User.user_id == user_id ).gino.one()
        if result:
            return True
        return False
