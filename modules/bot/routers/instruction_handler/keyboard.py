from aiogram.types import   (ReplyKeyboardMarkup,KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton, )




from modules.bot.utils.navigation import NavInstruction

# connect_button      = KeyboardButton(text=NavMain.CONNECT,      )
# information_button  = KeyboardButton(text=NavMain.INFORMATION,  )
# invite_button       = KeyboardButton(text=NavMain.INVITE,       )  

ios     = InlineKeyboardButton(text='IOS',callback_data=NavInstruction.IOS)
android = InlineKeyboardButton(text='Android',callback_data=NavInstruction.ANDROID)
windows = InlineKeyboardButton(text='Windows',callback_data=NavInstruction.WIDNOWS)
mac     = InlineKeyboardButton(text='Mac OS',callback_data=NavInstruction.MAC)
linux   = InlineKeyboardButton(text='Linux',callback_data=NavInstruction.LINUX)

instruction_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [ios,android],
    [windows,mac],
    [linux]])


def how_to_keyboard(app,deeplink,download_url):
    download_button = InlineKeyboardButton(text=f'☁️ Скачать {app}',url=download_url)
    add_button      = InlineKeyboardButton(text=f'⚙️ Добавить в {app}',url=deeplink) 
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            download_button
        ],
        [
            add_button
        ]
        ])
