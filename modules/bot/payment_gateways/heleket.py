import base64
import json
import logging
import hashlib
from uuid import uuid4

from aiogram.utils.i18n.context import gettext as _
from aiohttp.web import Request, Response

from modules.bot.models import purchase_data
from modules.bot.models.purchase_data import PurchaseData
from modules.bot.payment_gateways.gateway import PaymentGateway
from modules.bot.utils.navigation import NavPurshare
from modules.utils.constants import HELEKET_WEBHOOK
import requests



logger = logging.getLogger(__name__)

class HeleketGateway(PaymentGateway):
    callback = NavPurshare.PAY_HELEKET


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.name = _("payment_gateway_heleket")
        self.merchant = self.config.heleket.MERCHANT_UUID
        self.API_KEY = self.config.heleket.PAYMENT_API_KEY
        self.heleket_base_url = "https://api.heleket.com/v1/"
        self.app.router.add_post(HELEKET_WEBHOOK,self.webhook_handler)
        logger.info("Heleket payment gateway initialized")

    def generate_signature(self, data: str) -> str:
        base64_encoded = base64.b64encode(data.encode()).decode()
        raw_string = f"{base64_encoded}{self.API_KEY}"
        return hashlib.md5(raw_string.encode()).hexdigest()

    async def create_payment(self, purschare_data: PurchaseData) -> str:

        transaction_uuid = str(uuid4())
        data = {"amount":str(purschare_data.price),
                "currency":"RUB",
                "order_id": transaction_uuid,
                "url_callback": self.config.bot.DOMAIN+HELEKET_WEBHOOK
                }
        sign = self.generate_signature(json.dumps(data))
        logger.info(f"sign: {sign}")

        headers = {
            "merchant" : self.merchant,
            "sign" : sign 

        }
        url = self.heleket_base_url +  "payment"
        logger.info(f"heleket payment url : {url}")

        response = requests.post(url = url,
                                headers = headers,
                                json = data)


        
        await self._on_create_payment(
                session = self.session,
                tg_id       = purschare_data.user_id,
                payment_id  = transaction_uuid,
                days        = purschare_data.days,
        )
        logger.info(response.json())
        

        pay_url = response.json()['result']["url"]
        logger.info(f"payment link created for user : {purschare_data.user_id} : {pay_url}")
        return pay_url 

    async def handle_payment_succeeded(self, payment_id: str):
        await self._on_payment_succeeded(payment_id)
    
    async def handle_payment_canceled(self, payment_id: str):
        await self._on_payment_canceled(payment_id)

    async def validate_request(self,event: dict,request : Request):
            client_ip = (
                request.headers.get("CF-Connecting-IP")
                or request.headers.get("X-Real-IP")
                or request.headers.get("X-Forwarded-For")
                or request.remote
            )
            if client_ip not in ["31.133.220.8"]:
                logger.warning(f"Unauthorized IP: {client_ip}")
                #return False

            recieved_sign = event.pop("sign")
            logger.info(event)
            calculated_sign = self.generate_signature(json.dumps(event, separators=(",", ":")))
            logger.info(f"recieved : {recieved_sign}")
            logger.info(f"calculated : {calculated_sign}")
            if recieved_sign!=calculated_sign:
                logger.info("heleket webhook sign didnt match")
                return False
            return True
         

    async def webhook_handler(self, request: Request) -> Response:
        try:
            event_json  = await request.json()
            logger.info(event_json)
            logger.info(await request.read())
            if not await self.validate_request(event_json,request):
                return Response(status = 401)

            payment_id = event_json.get("order_id","")
            match event_json.get("status"):
                case "paid":
                    logger.info(f"{payment_id} paid")
                    await self.handle_payment_succeeded(payment_id=payment_id)
                    return Response(status = 200)
                case "cancel":
                    logger.info(f"{payment_id} canceled")
                    await self.handle_payment_canceled(payment_id=payment_id)
                    return Response(status = 200)
                case _:
                    return Response(status = 400)

        except Exception as e:
            logger.exception(f"error procceesing yookassa webhook : {e}")
            return Response(status=400)
        return Response(status=400)




        
