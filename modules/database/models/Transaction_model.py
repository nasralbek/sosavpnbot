from sqlalchemy import Column,BigInteger,Integer,String,DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

def create_transaction_model(db):
    class Transaction(db.Model):
        __tablename__ = "transactions"

        user_id         = Column(BigInteger)
        payment_id      = Column(UUID       ,   primary_key=True)
        url             = Column(String)
        amount          = Column(Integer)
        status          = Column(String     ,   default = "pending")
        days            = Column(Integer    ,   primary_key=True)
        created_at = db.Column(db.DateTime(), default=datetime.now)

        async def set_status(self,new_status):
            self.status = new_status
            print(self.status)
            await self.update(status = self.status).apply()
            print(self.status,"after")

        async def set_success(self):
            print("success")
            await self.set_status('success')

        async def set_canceled(self):
            await self.set_status('canceled')

        @classmethod
        async def create_transaction(cls,
                            user_id,
                            payment_id,
                            url, #?
                            amount,
                            days):
            payment_id = uuid.UUID(payment_id)
            new_transaction = await cls.create(user_id     = user_id    ,
                                                            payment_id  = payment_id ,
                                                            url         = url        ,
                                                            amount      = amount     ,
                                                            days = days)

        @classmethod
        async def get_pending_transactions(cls):
            transactions = await cls.query.where(cls.status == "pending").gino.all()
            return transactions
        
        @classmethod
        async def get_user_successful_transactions(cls, user_id: int):
            result = await cls.select('amount').where(
                            (cls.user_id == user_id) & 
                            (cls.status == "success")
                            ).gino.scalar() or 0
            return result

    return Transaction

