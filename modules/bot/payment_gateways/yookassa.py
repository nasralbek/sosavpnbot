
import logging
from aiogram.utils.i18n import gettext as _
from aiohttp.web import Request, Response
from yookassa.domain.common import SecurityHelper, response_object
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.models.receipt import Receipt, ReceiptItem
from yookassa.payment import PaymentRequest

from modules.bot.payment_gateways.gateway import PaymentGateway
from modules.bot.models import Plan,PurchaseData, purchase_data
from yookassa import Configuration,Payment 
from yookassa.domain.notification import (
    WebhookNotificationEventType,
    WebhookNotificationFactory,
)
from modules.bot.utils.navigation import NavPurshare
from modules.database.models.transaction import Transaction
from modules.utils.constants import YOOKASSA_WEBHOOK, TransactionStatus

logger = logging.getLogger(__name__)

class Yookassa(PaymentGateway):

    callback = NavPurshare.PAY_YOOKASSA

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.name = _("payment_gateway_yookassa")

        Configuration.configure(self.config.yookassa.SHOP_ID,self.config.yookassa.TOKEN)
        self.app.router.add_post(YOOKASSA_WEBHOOK,self.webhook_handler)
        logger.info("YooKassa payment gateway initialized")

    async def create_payment(self, purschare_data : PurchaseData) -> str:
        bot_username = (await self.bot.get_me()).username
        redirect_url = f"https://t.me/{bot_username}"
        #description = _()
        description = "some description"
        price = str(purschare_data.price)
            
        receipt = Receipt(
            customer = {"email":"dsadsadsa@dsdsa.ru"},
            items=[
                ReceiptItem(
                    description = description,
                    quantity    = 1,
                    amount      = {"value": price, "currency": "RUB"}, #TODO : self.currency.code
                    vat_code    = 1
                )
            ]
        )
        
        request = PaymentRequest(
            amount          = {"value" : price,"currency" : "RUB" },
            confirmation    = {"type":ConfirmationType.REDIRECT,"return_url": redirect_url},
            capture         = True,
            description     = description,
            receipt         = receipt
        ) 

        response = Payment.create(request)


        await self._on_create_payment(
                session     = self.session,
                tg_id       = purschare_data.user_id,
                payment_id  = response.id,
                days        = purschare_data.days, 

            )

        
        pay_url = response.confirmation["confirmation_url"]
        logger.info(f"payment link created for user : {purschare_data.user_id} : {pay_url}")
        return pay_url 

    async def handle_payment_succeeded(self,payment_id : str)-> None:
        logger.info(f"succeeded : {payment_id}")
        await self._on_payment_succeeded(payment_id)
    
    async def handle_payment_canceled(self, payment_id: str) -> None:
        await self._on_payment_canceled(payment_id)

    async def webhook_handler(self,request : Request) -> Response:
        ip = request.headers.get("X-Forwarded-For", request.remote)


        #TODO: uncomment
        #if not SecurityHelper().is_ip_trusted(ip):
        #    return Response(status=403)

        try:
            event_json = await request.json()
            notification_object = WebhookNotificationFactory().create(event_json)
            response_object = notification_object.object
            payment_id = response_object.id
            match notification_object.event:
                case WebhookNotificationEventType.PAYMENT_SUCCEEDED:
                    await self.handle_payment_succeeded(payment_id=payment_id)
                    return Response(status = 200)
                case WebhookNotificationEventType.PAYMENT_CANCELED:
                    await self.handle_payment_canceled(payment_id=payment_id)
                    return Response(status = 200)
                case _:
                    return Response(status = 400)

        except Exception as e:
            logger.exception(f"error procceesing yookassa webhook : {e}")
            return Response(status=400)
