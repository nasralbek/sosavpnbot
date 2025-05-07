from uuid import uuid4
from yookassa import Payment, Configuration
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from yookassa.domain.common import SecurityHelper
from enum import Enum
from var_dump import var_dump

from configs.main_config import YOOKASSA_CONFIG

class TransactionStatus(Enum):
    success     = 1
    canceled    = 2  

class PaymentData:
    def __init__(self,url,payment_id):
        self.url = url
        self.payment_id = payment_id

    def __str__(self):
        return f"PaymentData: {self.url} {self.payment_id}"

class YookassaManager():
    def __init__(self):
        Configuration.configure(YOOKASSA_CONFIG.YOOKASSA_ACCOUNT_ID,YOOKASSA_CONFIG.YOOKASSA_SECRET_KEY)

    def create_payment(self,user_id,price,) -> PaymentData:
        #uuid=str(uuid4())
        payment = Payment.create(
        {
            "amount": {
                "value": f"{price}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/dsaopdasdopsadsopasosavpntestbot"
            },
            "capture": True,
            "description": f"Заказ от пользователя : {user_id} ",
            "metadata": {
                "user_id": f"{user_id}"
            }
        })
        
        payment_id = payment.id
        url = payment.confirmation.confirmation_url
        payment_data = PaymentData(url,payment_id )
        return payment_data
    
    def check_transaction_status(self,payment_id):
        #TODO: implement
        payment_res = Payment.find_one(str(payment_id))
        status = str(payment_res.status)
        if status == "succeeded":
            return TransactionStatus.success
        elif status == "canceled":
             return TransactionStatus.canceled

