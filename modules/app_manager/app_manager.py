from modules.xuiAPI.xuiAPI import X_UI_API
from modules.databases.DB_GINO_MANAGER import DatabaseManager
from configs.main_config import REFERRAL_PROGRAMM_CONFIG 
from uuid import uuid4


class App_manager():
    def __init__(self):
        pass

    async def get_instance():
        self = App_manager()
        self.xui_api = X_UI_API()
        self.db_manager = await DatabaseManager.auth_from_config()
        return self    

    async def add_days_to_user(self,user_id,amount):
        self.xui_api.add_days(user_id,amount)
        self.db_manager.lirili_larila()


    async def register_user(self,user_id):
        uuid        = uuid4()
        user_in_xui = await self.register_in_xui(user_id,uuid)
        sub_id      = user_in_xui.sub_id
        expiry_time = user_in_xui.expiry_time
        await self.db_manager.register_user(user_id,uuid,sub_id,expiry_time)

    async def is_user_exists(self,user_id):
        await self.xui_api.get_user(user_id)
        return await self.db_manager.is_user_exists(user_id)

    async def new_referral(self,user_id,ref_id):
        user        = await self.db_manager.get_user(user_id)
        referral    = await self.db_manager.get_user(ref_id)
        user_expiry = await self.xui_api.increase_expiry_time(user,
                                                REFERRAL_PROGRAMM_CONFIG.BONUS_TO_INVITED)
        ref_expiry  = await self.xui_api.increase_expiry_time(referral,
                                                REFERRAL_PROGRAMM_CONFIG.BONUS_TO_INVITER)
        
        await user.set_expiry_time(user_expiry)
        await referral.set_expiry_time(ref_expiry)

        await user.set_referral(ref_id)
        await referral.increase_referrals(1)


    async def register_in_xui(self,user_id,uuid):
        user_in_xui = await self.xui_api.register_user(user_id,uuid)
        return user_in_xui

    async def register_in_database(self,
                                   user_id,
                                   uuid,
                                   sub_id):
        self.db_manager.register_user(user_id,uuid,sub_id)
        




