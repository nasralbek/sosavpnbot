# from yookassa import Configuration, Payment,Settings
# from uuid import uuid4
# from var_dump import var_dump
# #from modules.databases.transactions_db import Transactions_DB,Transaction_status
# #from modules.databases.keys_db import Keys_DB
# from configs.main_config import db_filename
# import asyncio

# from configs.main_config import YOOKASSA_CONFIG

# class Yookassa_handler():
#     def __init__(self):
#         Configuration.configure(YOOKASSA_CONFIG.YOOKASSA_ACCOUNT_ID,YOOKASSA_CONFIG.YOOKASSA_SECRET_KEY)
        
#         self.transactions_db = Transactions_DB(db_filename)
#         self.keys_db=Keys_DB(db_filename)


#     async def create_payment(self,user_id,price,):
#         uuid=str(uuid4())
#         payment = Payment.create(
#         {
#             "amount": {
#                 "value": f"{price}.00",
#                 "currency": "RUB"
#             },
#             "confirmation": {
#                 "type": "redirect",
#                 "return_url": "https://t.me/dsaopdasdopsadsopasosavpntestbot"
#             },
#             "capture": True,
#             "description": f"Заказ от пользователя : {user_id} ",
#             "metadata": {
#                 "user_id": f"{user_id}"
#             }
#         })

#         print(uuid)
#         #var_dump(payment)
#         payment_id = payment.id
#         url = payment.confirmation.confirmation_url
#         await self.transactions_db.create_transaction(user_id,price,uuid,payment_id)
#         return url
    
#     async def stop_background(self):
#         self.isRunning = False


#     async def start_check_payments(self):
#         self.isRunning = True
        
#         while self.isRunning:
#             try:
#                 uuids = await self.transactions_db.get_waiting_transactions()
#             except Exception as e:
#                 print("")
#             for uuid in uuids:
#                 try:
#                     payment_id = await self.transactions_db.get_payment_id(uuid)
#                     payment_res = Payment.find_one(payment_id)
#                     var_dump(payment_res)
#                     status = str(payment_res.status)
#                     #print(status)
#                     #print(status == "succeeded")

#                     if status == "succeeded":
#                             user_id = await self.transactions_db.get_user_id(uuid)
#                             await self.keys_db.add_pending(user_id)
#                             await self.transactions_db.set_transaction_status(uuid,Transaction_status.success)
#                             await self.transactions_db.set_key_requested(uuid,True)
#                     elif status == "canceled":
#                         await self.transactions_db.set_transaction_status(uuid,Transaction_status.canceled)
#                 except Exception as e:
#                         print (e)
#             await asyncio.sleep(1)
        
# # def test():
# #     yoo_handler = yookassa_handler()
# #     yoo_handler.create_payment(0000,100)
# #     yoo_handler.check_payments()
# #     print(uuid4())

# # if __name__ =="__main__":
# #     test()