from py3xui import AsyncApi, Client
import asyncio
from configs.main_config import DEFAULT_INBOUND
from datetime import datetime
import time
import random

def get_rand_sub(len=20):
    chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return str(''.join(random.choice(chars) for _ in range(len)))

def days_to_mseconds(days: int) -> int:
        return days*24*60*60*1000

class X_UI_API():
    def __init__(self):
        self.api = AsyncApi.from_env(use_tls_verify=True)
        asyncio.create_task(self.api.login())
   
    async def register_user(self,
                            user_id,
                            uuid,):
         
        #required fields 
        email       = user_id
        id          = uuid
        enable      = True
        flow        = "xtls-rprx-vision"
        #Optional_fields
        inbound_id  = self.get_defult_inbound_id()
        tg_id       = user_id
        expiry_time = int((time.time() + 7 * 24 * 60 * 60) * 1000)
        sub_id = get_rand_sub()
        new_client  = Client(id = str(uuid),
                                email=str(user_id),
                                enable=True,
                                tg_id = user_id,
                                expiry_time = expiry_time,
                                sub_id = sub_id,
                                flow = "xtls-rprx-vision"  )
        try:
            result = await self.api.client.add(inbound_id,[new_client])
            return new_client
        except Exception as e:
            print(f"эксептик то проходит, {e}")
            return await self.get_user(user_id)

    async def get_user(self,user_id):
        result = await self.api.client.get_by_email(str(user_id))
        return result
    
    async def get_total(self,user_id):
        await self.api.login()
        client = await self.api.client.get_by_email(str(user_id))
        if client.email == str(user_id):
            total = client.up + client.down
            return total

    async def add_days(self,user_id,amount):
        seconds = days_to_mseconds(amount)
        user = await self.get_user(user_id)
        now_time = int(time.time())*1000
        base = max(user.expiry_time,now_time)
        user.expiry_time = base + seconds
        self.api.client.update(user.id,user)

    async def increase_expiry_time(self,user,days_amount):
        tg_id = user.user_id
        client = await self.get_user(str(tg_id))
        seconds = days_to_mseconds(days_amount)
        client.expiry_time = max(int(time.time()*1000),client.expiry_time) + seconds
        client.id = str(user.uuid)
        client.sub_id = user.sub_id 
        client.enable = True
        client.flow = "xtls-rprx-vision"
        await self.api.client.update(client.id,client)        
        return client.expiry_time 


    def get_defult_inbound_id(self):
        return DEFAULT_INBOUND

    def get_defult_flow(self):
        return None
    
    def get_default_method(self):
        return None
    

    # async def get_key(self,uuid,user_id,inbound = DEFAULT_INBOUND):
    #     new_client = Client(id = uuid,email=f"tg_id:{user_id}",enable=True,tg_id = user_id,sub_id=get_rand_sub(),expiry_time = 30)
    #     reuslt = await self.api.client.add(inbound,[new_client])
    #     return f"https://sosavpn.tech:2096/sub/{new_client.sub_id}"