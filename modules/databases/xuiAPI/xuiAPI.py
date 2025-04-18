import os
from py3xui import AsyncApi, Client
import asyncio
from configs.main_config import default_inbound
import random

def get_rand_sub(len=20):
    chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return str(''.join(random.choice(chars) for _ in range(len)))

class X_UI_API():
    def __init__(self):
        self.api = AsyncApi.from_env(use_tls_verify=True)
        asyncio.create_task(self.api.login())
   
    
    
    async def get_key(self,uuid,user_id,inbound = default_inbound):
        new_client = Client(id = uuid,email=f"tg_id:{user_id}",enable=True,tg_id = user_id,sub_id=get_rand_sub(),expiry_time = 30)
        reuslt = await self.api.client.add(inbound,[new_client])
        return f"https://sosavpn.tech:2096/sub/{new_client.sub_id}"