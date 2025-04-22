from sqlalchemy import Column,BigInteger,Integer,String,DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

def create_user_model(db):
    class User(db.Model):
        __tablename__ = "users"

        user_id = Column(BigInteger,primary_key=True)
        payment_uuid = Column(UUID(as_uuid=True),primary_key=True)
        created_at = Column(DateTime,default = datetime.astimezone.utc)
        amount  = Column(Integer)
        status = Column(String, primary_key=True)
    return User