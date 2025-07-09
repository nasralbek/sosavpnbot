from datetime import timedelta
import logging
from abc import ABC, abstractmethod

from aiogram import Bot
from aiogram.utils.i18n import I18n
from aiogram.fsm.storage.redis import RedisStorage

from aiohttp.web import Application
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import Config
from modules.bot.models.purchase_data import PurchaseData
from modules.bot.models.services_container import ServicesContainer
from modules.database.models.transaction import Transaction
from modules.database.models.user import User
from modules.utils.constants import TransactionStatus

logger = logging.getLogger(__name__)

class PaymentGateway(ABC):
    name: str
    callback: str
    

    def __init__(
        self,
        app: Application,
        config: Config,
        session: async_sessionmaker,
        storage: RedisStorage,
        bot: Bot,
        i18n: I18n,
        services: ServicesContainer,
    ) -> None:
        self.app = app
        self.config = config
        self.session = session
        self.storage = storage
        self.bot = bot
        self.i18n = i18n
        self.services = services



    @abstractmethod
    async def create_payment(self, purschare_data: PurchaseData)-> str:
        pass

    @abstractmethod
    async def handle_payment_succeeded(self,payment_id : str):
        pass

    @abstractmethod 
    async def handle_payment_canceled(self,payment_id : str):
        pass


    async def _on_payment_succeeded(self,payment_id : str):
        logger.info(f"payment succeeded {payment_id}")
        inviter = None
        async with self.session() as session:
            transaction = await Transaction.get_by_id(session = session,payment_id = payment_id)
            days = transaction.days
            user = await User.get(session = session,tg_id = transaction.tg_id)
            await Transaction.update(
                session = session,
                payment_id=payment_id,
                status = TransactionStatus.COMPLETED
            )

            invited_by_id = user.invited_by
            if self.config.shop.REFERRER_REWARD_ENABLED and invited_by_id:
                inviter = await User.get(session = session, tg_id = invited_by_id)

        user_time_delta = timedelta(days = days)
        inviter_time_delta = user_time_delta*0.2
        #TODO: notify dev

        await self.services.notification.notify_payment_succeeded(user,transaction)
        
        await self.services.vpn.add_days(user,user_time_delta)
        if inviter and self.config.shop.REFERRER_REWARD_ENABLED:
            await self.services.vpn.add_days(inviter,inviter_time_delta)
            await self.services.notification.notify_referral_purschared(inviter,inviter_time_delta)



    async def _on_payment_canceled(self,payment_id : str):
        async with self.session() as session:
            transaction = await Transaction.get_by_id(session = session,payment_id = payment_id)
            
            await transaction.update(session=session,
                                     payment_id=payment_id,
                                     status=TransactionStatus.CANCELED)




















