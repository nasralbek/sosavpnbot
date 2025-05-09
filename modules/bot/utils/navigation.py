from enum import Enum
from aiogram.filters.callback_data import CallbackData

class NavMain(str,Enum):
    MAIN        = 'start'
    INVITE      = 'invite'
    CONNECT     = 'connect'
    INFORMATION = 'information'

class NavInstruction(str,Enum):
    MAIN    = 'how_to'
    IOS     = f'{MAIN}_ios'
    MAC     = f'{MAIN}_mac'
    WIDNOWS = f'{MAIN}_windows'
    ANDROID = f'{MAIN}_andorid'

class NavConnect(str,Enum):
    MAIN = 'connect'
    INSTRUCTIONS = f'{MAIN}_instructions'
    TOPUP = '{MAIN}_topup'

class NavInformation(str,Enum):
    MAIN = 'information'
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

