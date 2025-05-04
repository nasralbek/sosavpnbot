from sqlalchemy import Column,BigInteger,Integer,String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
import time
from math import ceil

def ms_to_days(ms):
    return ceil(ms/1000/60/60/24)

def create_user_model(db):
    class User(db.Model):
        __tablename__ = "users"

        user_id     = Column(BigInteger         ,primary_key = True)
        uuid        = Column(UUID ,primary_key = True)        
        invited_by  = Column(BigInteger         ,nullable    = True) 
        referrals   = Column(Integer            ,default     = 0   )
        expiry_time = Column(BigInteger         ,) 
        sub_id      = Column(String             ,)

        async def get_key(self):
            return f"https://sosavpn.tech:2096/sub/{self.sub_id}"

        async def get_remaining_days(self):
            now = int(time.time())*1000
            remaining = ms_to_days(self.expiry_time-now)
            if remaining > 0 or True:
                return remaining
            return 0

        async def get_expiry_time(self):
            return self.expiry_time

        async def set_expiry_time(self,new_expiry_time):
            self.expiry_time = new_expiry_time
            await self.update(expiry_time = self.expiry_time).apply()

        async def lirili_larila(self,days):
            expiry_time = max(self.expiry_time,time.time())+days*24*60*60
            await self.set_expiry_time(expiry_time)            

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

        async def get_referrals(self):
            return self.referrals
    return User


    