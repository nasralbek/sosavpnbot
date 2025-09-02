from datetime import datetime, timedelta,timezone
import aiogram
import asyncio

from aiogram.filters import callback_data
from aiogram.types import FSInputFile, InlineKeyboardButton, inline_keyboard_markup
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils import i18n, keyboard
from remnawave_api import RemnawaveSDK
from remnawave_api.models import UpdateUserRequestDto, UserResponseDto

from modules.bot.utils.navigation import NavMain, NavProfile
from config import DatabaseConfig
from modules.database.database import DataBase
from modules.database.models.user import User

db_host = "194.127.178.114"
db_port = 5432
db_name = "postgres"
db_username = "sosapostres"
db_pass = "raufartem777"
db_config = DatabaseConfig(
        db_host,
        db_port,
        db_name,
        db_username,
        db_pass
    )
db = DataBase(db_config) 



remnawave_url = "https://api.mysosa.xyz"
remnawave_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiNGUwY2NjZGQtM2JkNS00ZDE1LTk0OGMtMWMwMmUwNTM5OGZiIiwidXNlcm5hbWUiOm51bGwsInJvbGUiOiJBUEkiLCJpYXQiOjE3NTQzNDY3NDMsImV4cCI6MTAzOTQyNjAzNDN9.3z8_ACKlXx4M_XmVIgt5iTOD0jk403ibUX9o5uIbMNA" 

r_sdk = RemnawaveSDK(base_url= remnawave_url,token = remnawave_token)

markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "⚙️ Подключить VPN",callback_data=NavProfile.MAIN)],
    [InlineKeyboardButton(text = "🏠 Главное меню",callback_data=NavMain.MAIN)],
])

bot_token = "7518561707:AAGhfU3wyVR2Sf30u3Sk1e2Mxteb8UbBI-k"
bot = aiogram.Bot(token = bot_token)

message_text = "🎉 <b>С днем знаний! Вас ждет подарок!</b>\n\n\
❤️ Администрация Sosa желает Вам успехов в учёбе, работе и новых начинаниях.\n\n🎁 В честь праздника мы начислили Вам <b>3 дня к вашей VPN-подписке</b>."
invite                          = FSInputFile("src/purschare.JPEG")
async def pizdaliz_work(user: User,remna_user : UserResponseDto):
    await bot.send_photo(chat_id = user.tg_id,caption= message_text,reply_markup = markup,photo =invite,parse_mode = "html")
    if remna_user.expire_at < datetime.now(timezone.utc):
        await r_sdk.users.update_user(
            UpdateUserRequestDto(
                                uuid = user.uuid.__str__(),
                                expire_at = datetime.now(timezone.utc) + timedelta(days = 3)
        )
    )
    else:
        await r_sdk.users.update_user(
            UpdateUserRequestDto(
                                uuid = user.uuid.__str__(),
                                expire_at = remna_user.expire_at + timedelta(days = 3)
        )
    )

admins = [495527160,399365366]
async def pizdalizv2():
    async with db.session() as s: 
        users = await User.get_all(session = s)
    #async with db.session() as s:
       # users.append(await User.get(session = s,tg_id=495527160))
       # users.append(await User.get(session = s,tg_id = 399365366))
    k = 1
    m=len(users)
    errors = 0
    for user in users:
        try:
    
            remna_user = await r_sdk.users.get_user_by_uuid(user.uuid.__str__())
            if not isinstance(remna_user,UserResponseDto):
                continue
            if  not isinstance(remna_user.expire_at,datetime):
                continue
    
            will_add = (remna_user.expire_at - datetime.now(timezone.utc) < timedelta(days = -1)) or user.tg_id in admins
    
            print(f"{k}/{m}",user.tg_id,user.uuid,remna_user.expire_at,will_add)
            if will_add:
                await pizdaliz_work(user,remna_user)
            k+=1
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            errors +=1
            
    print(k-1,errors,m)
    

if __name__ == "__main__":
    asyncio.run(pizdalizv2())

