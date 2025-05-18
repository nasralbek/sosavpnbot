from modules.xuiAPI.xuiAPI import X_UI_API
from modules.database.database import DatabaseManager
from modules.yookassaAPI.yookassa_new import YookassaManager

from configs.main_config import REFERRAL_PROGRAMM_CONFIG 
from uuid import uuid4


class App_manager():
    def __init__(self,
                    xui_api         : X_UI_API,
                    db_manager      :DatabaseManager,
                    yookassa_manager:YookassaManager
                    ):
        self.xui_api            = xui_api
        self.db_manager         = db_manager
        self.yookassa_manager   = yookassa_manager

    @classmethod
    async def get_instance(cls) -> 'App_manager':
        xui_api             = X_UI_API()
        db_manager          = await DatabaseManager.auth_from_config()
        yookassa_manager    =  YookassaManager()
        return cls(xui_api,db_manager,yookassa_manager)    

    async def create_transaction(self,user_id,amount,days):
        payment_data = self.yookassa_manager.create_payment(user_id,amount)
        url,payment_id = payment_data.url, payment_data.payment_id
        await self.db_manager.Transaction.create_transaction(
                                    user_id,
                                    payment_id,
                                    url, #?
                                    amount,
                                    days)
        return url
    
    async def confirm_transaction(self,payment_id):
        transaction = self.db_manager.get_transaction(payment_id)
        transaction.set_success()

    async def cancel_transaction(self,payment_id):
        transaction = self.db_manager.get_transaction(payment_id)
        transaction.set_canceled()

    async def get_pending_transactions(self): 
        transactions = await self.db_manager.Transaction.get_pending_transactions() #TODO: MAKE 
        return transactions

    def check_transaction(self,payment_id):
        return self.yookassa_manager.check_transaction_status(payment_id)

    async def register_user(self,user_id):
        if await self.db_manager.User.is_exists(user_id):
            return
        uuid        = uuid4()
        user_in_xui = await self.register_in_xui(user_id,uuid)
        sub_id      = user_in_xui.sub_id
        expiry_time = user_in_xui.expiry_time
        await self.db_manager.User.register(user_id,uuid,sub_id,expiry_time)

    async def is_user_exists(self,user_id):
        await self.xui_api.get_user(user_id)
        return await self.db_manager.User.is_exists(user_id)
    
    async def get_user(self,user_id):
        return await self.db_manager.User.get(user_id)

    async def new_referral(self,user_id,ref_id):
        await self.add_days_to_user(user_id,REFERRAL_PROGRAMM_CONFIG.BONUS_TO_INVITED)
        await self.add_days_to_user(ref_id,REFERRAL_PROGRAMM_CONFIG.BONUS_TO_INVITER)

        user        = await self.db_manager.User.get(user_id)
        referral    = await self.db_manager.User.get(ref_id)
        await user.set_referral(ref_id)
        await referral.increase_referrals(1)

    async def add_days_to_user(self,user_id,days):
        user = await self.db_manager.User.get(user_id)
        user_expiry = await self.xui_api.increase_expiry_time(user, days)
        await user.set_expiry_time(user_expiry)

    async def register_in_xui(self,user_id,uuid):
        user_in_xui = await self.xui_api.register_user(user_id,uuid)
        return user_in_xui

    async def register_in_database(self,
                                   user_id,
                                   uuid,
                                   sub_id):
        self.db_manager.register_user(user_id,uuid,sub_id)
        




