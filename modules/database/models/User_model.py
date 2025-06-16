from sqlalchemy import Column,BigInteger,Integer,String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
import time
from math import ceil
from tools.users_enum import RegisterUserEnum
from sqlalchemy import exists
import datetime

def ms_to_days(ms):
    return ceil(ms/1000/60/60/24)

def create_user_model(db):
    class User(db.Model):
        __tablename__ = "users"

        user_id           = Column(BigInteger         ,primary_key = True)
        uuid              = Column(UUID ,primary_key = True)        
        invited_by        = Column(BigInteger         ,nullable    = True) 
        referrals         = Column(Integer            ,default     = 0   )
        expiry_time       = Column(BigInteger         ,) 
        sub_id            = Column(String             ,)
        registered_at     = db.Column(db.DateTime(), default=datetime.datetime.now)
        notify_day_before = Column(Boolean, default=False)  
        notify_day        = Column(Boolean, default=False)        
        notify_day_after  = Column(Integer, default=0)       

        async def get_key(self):
            return f"https://add.sosavpn.tech/sub/{self.sub_id}"
        

        async def get_remaining_days(self):
            now         = int(time.time())*1000
            remaining   = ms_to_days(self.expiry_time-now)
            if remaining > 0 or True:
                return remaining
            return 0

        async def set_expiry_time(self,new_expiry_time):
            self.expiry_time = new_expiry_time
            self.notify_day_before = False
            self.notify_day = False

            await self.update(
                expiry_time=self.expiry_time,
                notify_day_before=False,
                notify_day=False
            ).apply()   

        async def set_referral(self,referral_id):
            self.invited_by = referral_id
            await self.update(invited_by = self.invited_by).apply()

        async def increase_expiry_time(self,amount):
            await self.set_expiry_time(self.expiry_time+amount)

        async def set_referrals(self,new_referrals):
            self.referrals = new_referrals
            await self.update(referrals = self.referrals).apply()

        async def increase_referrals(self,amount):
            await self.set_referrals(self.referrals+amount)
        
        async def decrease_referrals(self,amount):
            await self.increase_referrals(-amount)
        
        @classmethod
        async def get_key_by_id(cls,user_id):
            user = await cls.get(user_id)
            return await user.get_key()


        @classmethod
        async def register(cls,user_id,uuid,sub_id,expiry_time):
            if await cls.is_exists(user_id):
                return RegisterUserEnum.user_already_exists
            new_user = await cls.create(       user_id    = user_id     ,
                                                uuid        = uuid       ,
                                                sub_id      = sub_id     ,
                                                expiry_time = expiry_time   )
            return RegisterUserEnum.register_success
            return new_user
        
        @classmethod
        async def add_referral(cls,user_id,referral_id):
            try:
                invited_user  = await cls.get_user(user_id)  
                referral_user = await cls.get_user(referral_id)
                await invited_user.set_referral(referral_id)
                await referral_user.increase_referrals(1)
            except Exception as e:
                print(e)

        @classmethod
        async def get(cls,user_id):
            user =  await cls.query.where(cls.user_id == user_id ).gino.one()
            return user

        @classmethod
        async def is_exists(cls,user_id) -> bool:
            result = await cls.query.where(cls.user_id == user_id).gino.first()
            return result is not None

    return User


    