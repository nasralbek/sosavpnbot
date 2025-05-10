from aiogram.types import   (ReplyKeyboardMarkup,KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton, )


from modules.bot.utils.navigation import NavMain

connect_button      = KeyboardButton(text=NavMain.CONNECT,      )
information_button  = KeyboardButton(text=NavMain.INFORMATION,  )
invite_button       = KeyboardButton(text=NavMain.INVITE,       )  

main_keyboard = ReplyKeyboardMarkup(keyboard=
    [
        [connect_button ],
        [
            invite_button,
            information_button,
        ]
    ],resize_keyboard=True)


