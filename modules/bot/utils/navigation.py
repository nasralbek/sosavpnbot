from enum import Enum
from aiogram.filters.callback_data import CallbackData

class NavMain(str,Enum):
    MAIN                = 'start'
    INVITE              = 'invite'
    PROFILE             = 'profile'
    SUPPORT             = 'support'
    CLOSE_NOTIFICATION  =  'close_notification'

class NavInvite(str,Enum):
    MAIN = NavMain.INVITE

class NavProfile(str,Enum):
    MAIN     = NavMain.PROFILE
    PURSHARE = 'purshare'

class NavSupport(str,Enum):
    MAIN = NavMain.SUPPORT 

class NavAdmin(str,Enum):
    MAIN = "admin"
    DISTR = "distribution"
    CANCEL_DISTR = "cancel_distr"
    CONFIRM_DISTR = "confirm_distr"


class NavPurshare:
    MAIN = NavProfile.PURSHARE
    CONFIRM = "confirm_purshare"
    PAY_YOOKASSA = "pay_yookassa"

class NavInstruction(str,Enum):
    MAIN    = 'how_to'
    IOS     = f'{MAIN}_ios'
    MAC     = f'{MAIN}_mac'
    WIDNOWS = f'{MAIN}_windows'
    ANDROID = f'{MAIN}_andorid'
    LINUX   = F'{MAIN}_linux'


class NavNotify(str,Enum):
    MAIN  = "notify"
    CLOSE = f"{MAIN}_close"
