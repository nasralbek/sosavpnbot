from aiogram.filters.callback_data import CallbackData

purshare_method_starter = "method_"
replenishment_callback = "replenishment"


class Purshare_plans:
    select_yookassa = "select_yookassa"
    select_start    = "select_stars"
    select_crypto   = "select_crypto"

class callbacks:
    profile_callback    = "profile"
    menu_callback       = "menu"



class how_to_callbacks:
    how_to_macos        = "how_to_macos"
    how_to_android      = "how_to_android"
    how_to_windows      = "how_to_windows"
    how_to_ios          = "how_to_ios"
    
    list = [how_to_macos,
            how_to_android,
            how_to_windows,
            how_to_ios] 


#   actions : select_method,select_method
#   method  : yookassa, stars,crypto, etc.
#   days    : days_count
#   price   :
class SelectMethodCallback(CallbackData,prefix = "method"):
    method  : str

class SelectDaysCallback  (CallbackData,prefix = "days"):
    method : str
    days   : int
