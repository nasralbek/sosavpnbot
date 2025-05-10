from configs.main_config import day_price
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


class BasePursharePlan():
    def __init__(self,days:int,):
        self.amount = days*day_price
        self.days = days

    def get_button_text(self):
        return f"{self.amount} руб. - {self.days} дней"

class TgPurshareYookasssaPlan(BasePursharePlan):
    def __init__(self,days):
        super().__init__(days)
        self.callback = f"select_yookassa_days_{days}"

class TgPurshareMethod():
    def __init__(self,name):
        self.name = name
        self.callback = f"select_{name}"
    
    def get_button_text(self):
        return f"{self.name}"

    def get_button(self):
        return InlineKeyboardButton(text = self.get_button_text(),
                                    callback_data=self.callback )

class TgPurshareMethodList():
    def __init__(self,*args):
        self.methods_list = [*args]

    def get_keyboard(self):
        keyboard = []
        for method in self.methods_list:
            keyboard.append([method.get_button()])
        return InlineKeyboardMarkup(keyboard)

purshare_methods = TgPurshareMethodList(
    TgPurshareMethod("💳 Банковской картой"),
    TgPurshareMethod("stars"),
    TgPurshareMethod("crypto")
)

