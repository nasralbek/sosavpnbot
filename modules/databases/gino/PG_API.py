from uuid import uuid4
from gino import Gino
import sqlalchemy as sa
from datetime import datetime
import random

db = Gino()

DEFAULT_PROTOCOL = "https"
DEFAULT_DOMAIN = "1.1.1.1"
DEFAULT_PORT = "1111"
DEFAULT_SUB_ID = lambda : rand_sub_id()

DEFAULT_DAYS = 0
DEFAULT_DEVICES = 5

def rand_sub_id(len=20):
    chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return str(''.join(random.choice(chars) for _ in range(len)))


class User(db.Model):
    tablename = 'users'

    user_id = db.Column(db.BigInteger(), primary_key=True)
    bonuses = db.Column(db.Integer(), default=0)
    invited_by = db.Column(db.BigInteger(), nullable=True)
    refferals = db.Column(db.Integer(),default = 0)
    key_uuid = db.Column(db.String())


class Key(db.Model):
    tablename = 'keys'
    key_uuid = db.Column(db.String(),primary_key=True)

    protocol = db.Column(db.String() ,default = DEFAULT_PROTOCOL)
    domain   = db.Column(db.String() ,default = DEFAULT_DOMAIN)
    port     = db.Column(db.Integer(),default = DEFAULT_PORT)
    sub_id   = db.Column(db.String() ,default = DEFAULT_SUB_ID())


class KeysParameter(db.Model):
    tablename = 'keys_parameter'

    key_uuid = db.Column(db.String(),primary_key=True)
    days = db.Column(db.Integer(),default = DEFAULT_DAYS)
    start_time = db.Column(db.DateTime(),nullable = True)
    expire_time = db.Column(db.DateTime(),nullable = True)
    devices = db.Column(db.Integer(),default = DEFAULT_DEVICES)


class Transaction(db.Model):
    tablename = 'transactions'

    created_at = db.Column(db.DateTime(),
                            default=datetime.astimezone.utc)
    local_id = db.Column(db.String())
    uuid = db.Column(db.String(), primary_key=True)
    payment_id = db.Column(db.String(),primary_key=True)
    amount = db.Column(db.Int())
    status = db.Column(db.String())


class Notification(db.Model):
    tablename = 'notifications'

    user_id = db.Column(db.BigInteger())
    notify_type = db.Column(db.String())
    notified = db.Column(db.Boolean())
    uuid = db.Column(db.String())


class PayedNotification(db.Model):
    tablename = 'payed_notifications'
    uuid = db.Column(db.String(), primary_key=True)
    new_expire_time = db.Column(db.DateTime())




class PG_GINO_API():
    def __init__():
        pass


    async def register_user(self,user_id,bonuses,invited_by,refferrals):
        user = await User.Create(
            user_id=user_id,
            bonuses=bonuses,
            invited_by = invited_by,
            refferrals=refferrals)
        key_uuid = user.key_uuid
        key = await Key.create(key_uuid = key_uuid)
        key_parameters = await KeysParameter.create(key_uuid = key_uuid)
    