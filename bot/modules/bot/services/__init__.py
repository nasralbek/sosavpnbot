from __future__ import annotations

from aiogram import Bot
from aiogram.fsm.storage.redis import RedisStorage
from remnawave_api import RemnawaveSDK
from sqlalchemy.ext.asyncio import async_sessionmaker

from typing import TYPE_CHECKING

from tools.image_container import ImageContainer
if TYPE_CHECKING:
    from modules.bot.models import ServicesContainer

from config import Config

from .plan import PlanService
from .vpn import VPNService
from .notification import NotificationService

async def initialize(
    config: Config,
    session: async_sessionmaker,
    bot: Bot,
    storage : RedisStorage,
    r_sdk : RemnawaveSDK,
    images : ImageContainer
) -> "ServicesContainer":
    from modules.bot.models import ServicesContainer
    # server_pool = ServerPoolService(config=config,
    #                                  session=session)
    
    plan = PlanService()

    vpn = VPNService(   config  =config,
                        session =session,
                        r_sdk   = r_sdk)
    
    notification = NotificationService( storage = storage,
                                        config  = config, 
                                        bot     = bot,
                                        images  = images,
                                        session = session)
    
    # referral = ReferralService(config=config, 
    #                            session_factory=session, 
    #                            vpn_service=vpn)
    
    # subscription = SubscriptionService(config=config, 
    #                                    session_factory=session, 
    #                                    vpn_service=vpn)

    return ServicesContainer(
        # server_pool=server_pool,
        plan=plan,
        vpn=vpn,
        notification=notification,
        # referral=referral,
        # subscription=subscription,
    )
