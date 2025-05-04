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

replenishment_button = InlineKeyboardButton(
    text = "пополнить баланс",
    callback_data = callbacks.replenishment_callback 
)

class PurshareMethodButtons():
    def __init__(self,days):
        self.yookassa = InlineKeyboardButton(text="Оплатить через yookassa", callback_data="confirm_vpn_yoomoney_{days}")
        self.balance  = InlineKeyboardButton(text="Оплатить с баланса", callback_data="confirm_vpn_bonuses_{days}")

class MainBotKeyboards():
    main_keyboard = ReplyKeyboardMarkup(keyboard=
        [
            [
                MainKeyboardsButtons.profile_button,
                MainKeyboardsButtons.information_button,
                MainKeyboardsButtons.connect_vpn_button, 
            ]
        ],resize_keyboard=True)
    
    information_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InfromationButtons.instrucions_button],
        [InfromationButtons.support_button]
    ])


    purshare_keyboard = InlineKeyboardMarkup(inline_keyboard=
        [
            #[InlineKeyboardButton(text="7 дней — 50₽", callback_data="confirm_vpn_7")],
            [PurshareKeyboardButtons.one_mounth_button]
        ]
    )

    connect_vpn_keyboard = InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InstructionsButtons.ios,
                InstructionsButtons.android
            ],
            [
                InstructionsButtons.macos,
                InstructionsButtons.windows
            ],
            [replenishment_button]
        ]
    )
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
                [stars_button   ],
                [crypto_button  ]
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

