
from dataclasses import dataclass

from modules.bot.services.plan import PlanService

@dataclass
class ServicesContainer:
    # server_pool: ServerPoolService
    plan: PlanService
    # vpn: VPNService
    # notification: NotificationService
    # referral: ReferralService
    # subscription: SubscriptionService
    pass
