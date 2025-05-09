from aiogram.types import ( ReplyKeyboardMarkup,
                            KeyboardButton,

                            InlineKeyboardButton,
                            )
from aiogram.utils.keyboard import InlineKeyboardBuilder
from modules.bot.utils.navigation import NavConnect,NavInformation

button = KeyboardButton(text = '',callback_data='')

invite_keyboard = ReplyKeyboardMarkup(keyboard=[[
    button
]])

class connect_vpn_keyboard:
    def __init__(self):
        builder = InlineKeyboardBuilder()
        
        instructions_button = InlineKeyboardButton(text = "инструкция",
                        callback_data = NavConnect.INSTRUCTIONS )
        replenishment_button = InlineKeyboardButton(
                        text = "пополнить баланс",
                        callback_data = NavConnect.TOPUP 
                    )
        builder.add(instructions_button)
        builder.add(replenishment_button)
        builder.adjust(1)
        self.keyboard = builder.as_markup()

    def get(self):
        return self.keyboard
    

class information_keyboard:
    def __init__(self):
        builder = InlineKeyboardBuilder()
        
        support_button = InlineKeyboardButton(text = 'instr',callback_data = NavInformation.INSTRUCTIONS )
        instructions_button = InlineKeyboardButton(text = 'support',url = "t.me/sosasupport" )
        builder.add(instructions_button)
        builder.add(support_button)
        builder.adjust(1)

        self.keyboard = builder.as_markup()
    
    def get(self):
        return self.keyboard