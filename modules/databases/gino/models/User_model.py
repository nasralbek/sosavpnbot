from sqlalchemy import Column,BigInteger,Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid

def create_user_model(db):
    class User(db.Model):
        __tablename__ = "users"

        user_id = Column(BigInteger,primary_key=True)
        balance = Column(Integer,default = 0)
        invited_by = Column(BigInteger,nullable = True)
        referrals  = Column(Integer,default = 0)
        key_uuid = Column(UUID(), primary_key=True)


        async def set_balance(self,new_balance):
            self.balance = new_balance
            await self.update(balance = self.balance).apply()


        async def increase_balance(self,amount):
            await self.set_balance(self.balance+amount)

        async def decrease_balance(self,amount):
            await self.increase_balance(-amount)

        async def set_referrals(self,new_referrals):
            self.referrals = new_referrals
            await self.update(referrals = self.referrals).apply()

        async def increase_referrals(self,amount):
            await self.set_referrals(self.referrals+amount)
        
        async def decrease_referrals(self,amount):
            await self.increase_referrals(-amount)
    return User


    