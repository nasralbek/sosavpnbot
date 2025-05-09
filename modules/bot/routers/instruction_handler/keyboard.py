from aiogram.types import   (ReplyKeyboardMarkup,KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton, )




from modules.bot.utils.navigation import NavInstruction

# connect_button      = KeyboardButton(text=NavMain.CONNECT,      )
# information_button  = KeyboardButton(text=NavMain.INFORMATION,  )
# invite_button       = KeyboardButton(text=NavMain.INVITE,       )  

ios     = InlineKeyboardButton(text='ios',callback_data=NavInstruction.IOS)
android = InlineKeyboardButton(text='android',callback_data=NavInstruction.ANDROID)
windows = InlineKeyboardButton(text='windows',callback_data=NavInstruction.WIDNOWS)
mac     = InlineKeyboardButton(text='macos',callback_data=NavInstruction.MAC)

instruction_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [ios,android],
    [windows,mac],])


def how_to_keyboard(app,deeplink,download_url):
    download_button = InlineKeyboardButton(text=f'скачать {app}',url=download_url)
    add_button      = InlineKeyboardButton(text=f'Добавить в {app}',url=deeplink) 
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            download_button
        ],
        [
            add_button
        ]
        ])
