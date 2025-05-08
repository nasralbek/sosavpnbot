from aiogram.types import ( ReplyKeyboardMarkup,
                            KeyboardButton,
                            InlineKeyboardMarkup,
                            InlineKeyboardButton,
                            )
from configs.main_config import day_price,default_plans
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.bot.keyboard_texts import *
import modules.bot.callbacks as callbacks
from math import ceil

class BackButton():
    def __init__(self,back):
        self.button  = InlineKeyboardButton(text = "Назад",callback_data = back)

    def get(self):
        return self.button


class MainKeyboardsButtons():
    connect_vpn_button  = KeyboardButton(
        text=MainKeyboardTexts.connect_vpn_text)
    information_button  = KeyboardButton(
        text=MainKeyboardTexts.information_text)
    profile_button      = KeyboardButton(
        text=MainKeyboardTexts.profile_text)

class PurshareKeyboardButtons():
    one_mounth_button = InlineKeyboardButton(
                            text          = PurshareKeyboardTexts.one_mounth_text,
                            callback_data = PurshareKeyboardTexts.one_mount_callback_data
                            )

class InfromationButtons():
    instrucions_button = InlineKeyboardButton(text='instr',callback_data="instr")
    support_button     = InlineKeyboardButton(text='support',callback_data="support")

class InstructionsButton():
    def __init__(self,back): 
        self.InstructionsButton = InlineKeyboardButton(text = 'Установить vpn',callback_data = callbacks.InstructionsCallback(back = back).pack())
    def get(self):
        return  self.InstructionsButton

class InstructionsButtons():
    ios     = InlineKeyboardButton(
                    text="📱 iOS",
                    callback_data=callbacks.how_to_callbacks.how_to_ios
                    )
    android = InlineKeyboardButton(
                    text="🤖 Android",
                    callback_data=callbacks.how_to_callbacks.how_to_android
                    )
    windows = InlineKeyboardButton(
                    text="🪟 Windows",
                    callback_data=callbacks.how_to_callbacks.how_to_windows
                    )
    macos   = InlineKeyboardButton(
                    text="💻 MacOS",
                    callback_data=callbacks.how_to_callbacks.how_to_macos
                    )

menu_button = InlineKeyboardButton(
                    text="Меню",
                    callback_data="menu"
                    )

class PurshareMethodButtons():
    def __init__(self,days):
        self.yookassa = InlineKeyboardButton(text="Оплатить через yookassa", callback_data="confirm_vpn_yoomoney_{days}")
        self.balance  = InlineKeyboardButton(text="Оплатить с баланса", callback_data="confirm_vpn_bonuses_{days}")

class MainBotKeyboards():
    main_keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [MainKeyboardsButtons.connect_vpn_button, ],
            [
                MainKeyboardsButtons.profile_button,
                MainKeyboardsButtons.information_button,
                
            ]
        ],resize_keyboard=True)
    
    class purshare_method_keyboard():

        yookassa_button = InlineKeyboardButton(
            text = 'yookassa',                                   
            callback_data = callbacks.SelectMethodCallback(method = "yookassa").pack())
        
        stars_button    = InlineKeyboardButton(
            text = 'stars',
            callback_data=callbacks.SelectMethodCallback(method = "stars").pack()   )
        crypto_button   = InlineKeyboardButton(
            text = 'crypto',
            callback_data=callbacks.SelectMethodCallback(method = "crypto").pack()  )
        keyboard = InlineKeyboardMarkup(inline_keyboard=
            [
                [yookassa_button],
                # [stars_button   ],
                # [crypto_button  ]
            ]
    )

    class information_keyboard:
        def __init__(self):
            builder = InlineKeyboardBuilder()
            
            instructions_button = InstructionsButton('information').get()
            support_button = InfromationButtons.support_button
            builder.add(instructions_button)
            builder.add(support_button)
            builder.adjust(1)

            self.keyboard = builder.as_markup()
        
        def get(self):
            return self.keyboard
            
    class connect_vpn_keyboard:
        def __init__(self):
            builder = InlineKeyboardBuilder()
            
            instructions_button = InstructionsButton('connect_vpn').get()
            replenishment_button = InlineKeyboardButton(
                            text = "пополнить баланс",
                            callback_data = callbacks.replenishment_callback 
                        )
            builder.add(instructions_button)
            builder.add(replenishment_button)
            builder.adjust(1)
            self.keyboard = builder.as_markup()

        def get(self):
            return self.keyboard


    class InstructionsKeyboard:
        def __init__(self,back):
            builder = InlineKeyboardBuilder()

            builder.add(InstructionsButtons.ios)
            builder.add(InstructionsButtons.android)
            builder.add(InstructionsButtons.macos)
            builder.add(InstructionsButtons.windows)

            builder.adjust(2)
            builder.add(BackButton(back).get())
            self.keyboard = builder.as_markup()

        def get(self):
            return self.keyboard


    purshare_keyboard = InlineKeyboardMarkup(inline_keyboard=
        [
            #[InlineKeyboardButton(text="7 дней — 50₽", callback_data="confirm_vpn_7")],
            [PurshareKeyboardButtons.one_mounth_button]
        ]
    )

    
    profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[[menu_button]])
    
    class days_keyboard():
        def __init__(self,method):
            builder = InlineKeyboardBuilder()
            for plan in default_plans:
                button = InlineKeyboardButton(
                    text = f"{plan} дней - {ceil(plan*day_price)} руб.",
                    callback_data  = callbacks.SelectDaysCallback(
                        days = plan,
                        method = method
                    ).pack()   
                )
                builder.add(button)
            builder.adjust(1)
            self.keyboard = builder.as_markup()

    class confirm_keyboard():
        def __init__(self,days,method):
            builder = InlineKeyboardBuilder()
            confirm_button = InlineKeyboardButton(text = "confirm",
                                                  callback_data = callbacks.ConfirmCallback(days=days,
                                                                                            method=method).pack()
                                                  )
            builder.add(confirm_button)
            builder.adjust(1)
            self.keyboard = builder.as_markup()
