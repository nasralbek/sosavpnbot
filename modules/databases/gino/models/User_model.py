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
        key_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    return User