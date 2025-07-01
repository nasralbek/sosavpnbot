from enum import Enum
from aiogram.filters.callback_data import CallbackData

class NavMain(str,Enum):
    MAIN                = 'start'
    INVITE              = '👥 Пригласить друга'
    CONNECT             = '⚙️ Подключить VPN'
    SUPPORT             = 'ℹ️ Информация'
    CLOSE_NOTIFICATION  =  'close_notification'

class NavSupport(str,Enum):
    MAIN = NavMain.SUPPORT 

class NavInvite(str,Enum):
    MAIN = NavMain.INVITE

class NavAdmin(str,Enum):
    MAIN = "admin"

class NavInstruction(str,Enum):
    MAIN    = 'how_to'
    IOS     = f'{MAIN}_ios'
    MAC     = f'{MAIN}_mac'
    WIDNOWS = f'{MAIN}_windows'
    ANDROID = f'{MAIN}_andorid'
    LINUX   = F'{MAIN}_linux'

class NavConnect(str,Enum):
    MAIN = NavMain.CONNECT
    INSTRUCTIONS = f'{MAIN}_instructions'
    TOPUP = '{MAIN}_topup'

class NavInformation(str,Enum):
    MAIN = 'ℹ️ Информация'
    INSTRUCTIONS = f'{MAIN}_instructions'

class NavConfirm(CallbackData,prefix = 'confirm'):
    method  : str
    days    : int
    price   : int

class NavPurshareMethod(CallbackData,prefix = 'method'):
    method  : str
    days    : int
    price   : int

class NavDaysCount(CallbackData,prefix = 'select_days'):
    days    : int
    price   : int

