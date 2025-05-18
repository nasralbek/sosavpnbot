from aiogram.types import   (ReplyKeyboardMarkup,KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton, )
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.bot.utils.navigation import NavPurshareMethod,NavDaysCount,NavConfirm
#from configs.main_config import enabled_purshare_methods,default_plans


from modules.bot.utils.navigation import NavMain
from modules.bot.utils.converter import Converter


connect_button      = KeyboardButton(text=NavMain.CONNECT,      )
information_button  = KeyboardButton(text=NavMain.INFORMATION,  )
invite_button       = KeyboardButton(text=NavMain.INVITE,       )  


# def select_method_keyboard(days,price) -> InlineKeyboardMarkup:
    # builder = InlineKeyboardBuilder()
    # for purshare_method in enabled_purshare_methods:
    #     builder.add(
    #         InlineKeyboardButton(text=purshare_method,
    #                              callback_data=NavPurshareMethod(method = purshare_method,days=days,price=price).pack()
    #                              )
    #     )
    # return builder.as_markup()

        
# def topup_keyboard()-> InlineKeyboardMarkup:
    # builder = InlineKeyboardBuilder()
    # for plan in default_plans:
    #     price = Converter.days2price(plan)
    #     button_text = f'{price}₽'
    #     builder.add(
    #         InlineKeyboardButton(text = button_text ,
    #                             callback_data = NavDaysCount(days=plan,price=price).pack()
    #                              )
    #     )
    #     builder.adjust(1)
    # return builder.as_markup()


def method_selected_keyboard(days,price,method,url) -> InlineKeyboardMarkup:
    confirm_button = InlineKeyboardButton(text = '🔗 Перейти к оплате',
                                          url = url)
    instructions_button = InlineKeyboardButton(text = '👨🏼‍💻 Техническая поддержка',url = "t.me/sosasupport" )
    return InlineKeyboardMarkup(inline_keyboard=[[confirm_button],[instructions_button]])



