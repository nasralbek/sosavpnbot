

from modules.bot.services import (
        #NotificationService,
        PlanService,
        #ServerPoolService,
        VPNService,
        #ReferralService,
        #SubscriptionService,
        #PaymentStatsService,
        #InviteStatsService,
)

from dataclasses import dataclass



@dataclass
class ServicesContainer:
    #server_pool: ServerPoolService
    plan: PlanService
    vpn: VPNService
    #notification: NotificationService
    #referral: ReferralService
    #subscription: SubscriptionService
    #payment_stats: PaymentStatsService
    #invite_stats: InviteStatsService


