
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n
from aiohttp.web import Application
from sqlalchemy.ext.asyncio import async_sessionmaker
from config import Config
from modules.bot.models.services_container import ServicesContainer
from modules.bot.payment_gateways.gateway import PaymentGateway
from modules.bot.payment_gateways.heleket import HeleketGateway
from modules.bot.payment_gateways.pally import PallyGateway
from modules.bot.payment_gateways.yookassa import Yookassa


class GatewayFactory:
    def __init__(self) -> None:
        self._gateways: dict[str,PaymentGateway]={}

    def register_gateway(self,gateway : PaymentGateway):
        self._gateways[gateway.callback] = gateway
    
    def get_gateway(self, name: str) -> PaymentGateway:
        gateway = self._gateways.get(name)
        if not gateway:
            raise ValueError(f"gateway {name} not registered")
        return gateway

    def get_gateways(self) -> list[PaymentGateway]:
        return list(self._gateways.values())


    def register_gateways(self,
                            app: Application,
                            config: Config,
                            session: async_sessionmaker,
                            storage: RedisStorage,
                            bot: Bot,
                            i18n: I18n,
                            services: ServicesContainer
                          ):
        dependencies = [app,config,session,storage,bot,i18n,services]

        gateways = [
            (config.shop.PAYMENT_YOOKASSA_ENABLED,Yookassa),
            (config.shop.PAYMENT_HELEKET_ENABLED,HeleketGateway),
            (config.shop.PAYMENT_PALLY_ENABLED, PallyGateway)
            #todo: add other
        ]

        for enabled,gateway_cls in gateways:
            if enabled:
                self.register_gateway(gateway_cls(*dependencies))


