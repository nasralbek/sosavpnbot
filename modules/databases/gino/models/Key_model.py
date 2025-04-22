from sqlalchemy import Column,BigInteger,Integer,String,DateTime,null
from sqlalchemy.dialects.postgresql import UUID
import uuid
import random

def rand_sub_id(len=20):
    chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    return str(''.join(random.choice(chars) for _ in range(len)))

DEFAULT_DEVICES_COUNT = 5
DEFAULT_PROTOCOL = "https"
DEFAULT_PORT = null
DEFAULT_DOMAIN = "sosavpn.tech"

def create_key_model(db):
    class Key(db.Model):
        __tablename__ = "keys"

        user_id  = Column(BigInteger,primary_key=True)
        key_uuid = Column(UUID(as_uuid=True), primary_key=True)
        domain   = Column(String,default = DEFAULT_DOMAIN)
        protocol = Column(String, default = DEFAULT_PORT )
        port     = Column(Integer,default=DEFAULT_PORT,nullable = True)


    return Key