
import hashlib
import logging
from uuid import uuid4
from aiogram import Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import gettext as _
from aiohttp.web import Application, Request, Response
import requests
from sqlalchemy.ext.asyncio import async_sessionmaker
from config import Config
from modules.bot.models.purchase_data import PurchaseData
from modules.bot.models.services_container import ServicesContainer
from modules.bot.payment_gateways.gateway import PaymentGateway
from modules.bot.utils.navigation import NavPurshare
from modules.utils.constants import PALLY_WEBHOOK


logger = logging.getLogger(__name__)

class PallyGateway(PaymentGateway):


    callback = NavPurshare.PAY_PALLY

    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.name       = _("payment:gateway:pally")
        self.app.router.add_post(PALLY_WEBHOOK,self.webhook_handler)
        self.API_URL_BASE = "https://pal24.pro"

        self.API_TOKEN  = self.config.pally.API_TOKEN 
        self.shop_id    = self.config.pally.SHOP_ID 
        logger.info("Pally payment gateway initialized")


    async def create_payment(self, purschare_data : PurchaseData) -> str:
        transaction_uuid = str(uuid4())


        url = f"{self.API_URL_BASE}/api/v1/bill/create"
        data = {
            "amount"    : str(purschare_data.price),
            "shop_id"   : self.shop_id,
            "order_id"  : transaction_uuid,    

        }
        headers = {"Authorization": f"Bearer {self.API_TOKEN}"}
        response = requests.post(url = url,
                                headers= headers,
                                json = data,
                                 )
        await self._on_create_payment(
                session = self.session,
                tg_id       = purschare_data.user_id,
                payment_id  = transaction_uuid,
                days        = purschare_data.days,
        )
        logger.info(response.json())
        pay_url = response.json()['link_page_url']
        logger.info(f"payment link created for user : {purschare_data.user_id} : {pay_url}")
        return pay_url 


    async def handle_payment_succeeded(self,payment_id : str)-> None:
        logger.info(f"succeeded : {payment_id}")
        await self._on_payment_succeeded(payment_id)
    
    async def handle_payment_canceled(self, payment_id: str) -> None:
        await self._on_payment_canceled(payment_id)


    async def validate_request(self,event: dict):
        recieved_sign = event["SignatureValue"]
        calculated_sign = hashlib.md5(
            f"{event["OutSum"]}:{event["InvId"]}:{self.API_TOKEN}".encode()
        ).hexdigest().upper()
        if recieved_sign!= calculated_sign:
            logger.info(f"signature didn`t match : recieved {recieved_sign},\n\
                        calculated : {calculated_sign}")
            return False
        return True


        
    async def webhook_handler(self, request : Request) -> Response:
        logger.info("pally webhook")
        logger.info(request)
        try:
            form_data = await request.post()
            event_json = dict(form_data)

            logger.info(event_json)
            logger.info(await request.read())
            if not await self.validate_request(event_json):
                return Response(status = 401)

            payment_id = event_json.get("InvId","")
            match event_json.get("Status"):
                case "SUCCESS":
                    logger.info(f"{payment_id} paid")
                    await self.handle_payment_succeeded(payment_id=payment_id)
                    return Response(status = 200)
                case "FAIL":
                    logger.info(f"{payment_id} canceled")
                    await self.handle_payment_canceled(payment_id=payment_id)
                    return Response(status = 200)
                case _:
                    return Response(status = 400)

        except Exception as e:
            logger.exception(f"error procceesing heleket webhook : {e}")
            return Response(status=400)





