from sqlalchemy import Column,BigInteger,Integer,String,DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
import random

def rand_sub_id(len=20):
    chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    return str(''.join(random.choice(chars) for _ in range(len)))

DEFAULT_DEVICES_COUNT = 5


def create_key_model(db):
    class Key(db.Model):
        __tablename__ = "keys"

        user_id = Column(BigInteger,primary_key=True)
        key_uuid = Column(UUID(as_uuid=True), primary_key=True)
        remaining_days =  Column(Integer, default=0)
        start_time = Column(DateTime,nullable = True)
        expite_time = Column(DateTime,nullable = True)
        devices = Column(Integer,default = DEFAULT_DEVICES_COUNT)

    return Key