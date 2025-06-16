from math import ceil
import time
from datetime import date


def gen_reflink(botname,user_id):
    return f"https://t.me/{botname}?start={user_id}"

def profile_text(user,botname):
    user_id  = user.user_id
    refs     = user.referrals
    topup_by_refs = refs*24    

    refilnk = gen_reflink(botname,user_id)

    return (
        #f"Ваш id: <b>{user_id}</b>\n"
        f"⚡️ <b>Вы получите 10 дней на Ваш баланс, если приглашенный друг пополнит свой баланс на любое количество дней.</b>\n\n"
        f"Например, если Вы пригласите 3 друга, которые будут ежемесячно пополнять баланс, то за наш сервис Вам платить не придется вообще.\n\n"
        f"👥 <b>Всего приглашено вами:</b> <code>{refs} чел.</code>\n"
        f"🔗 <b>Ссылка для приглашения:</b> {refilnk}\n"
    )

def connect_text(key,expiry_time, user):
    price = 3.33
    remaining_days = ceil((expiry_time - time.time()*1000)/1000/24/60/60)
    user_id  = user.user_id
    balance = ceil(remaining_days*price)
    expiry_date = date.fromtimestamp(expiry_time/1000)
    day = expiry_date.day
    month = expiry_date.month
    year = expiry_date.year
    expiry_date_text = f"{day}.{0 if month <10 else ''}{month}.{year}"
    #TODO FIX CRINGE
    #TODO FIX CRINGE
    #TODO FIX CRINGE
    #TODO FIX CRINGE
    #TODO FIX CRINGE
    #TODO FIX CRINGE
    #TODO FIX CRINGE
    #TODO FIX CRINGE
    #TODO: add balance (with days)

    result_text =""
    if remaining_days>0:
        result_text+=f"<b>🏠 Личный кабинет</b>\n"
        result_text+=f"├ Ваш ID: <b>{user_id}</b>\n"
        result_text+=f"└ Ваш баланс: <b>{remaining_days} дней</b>\n\n"
        #result_text+=f"🗝 <b>Ваш ключ:</b> <blockquote><code>{key}</code></blockquote>\n\n"
    else:
        result_text+=f"<b>🏠 Личный кабинет</b>\n"
        result_text+=f"├ Ваш ID: <b>{user_id}</b>\n"
        result_text+=f"└ Ваш баланс: <b>0 дней</b>\n\n"
        #result_text+=f"🗝 <b>Ваш ключ:</b> <blockquote><code>{key}</code></blockquote>\n\n"
    return result_text

information_text = (
"<b>1. Могу ли я использовать VPN на нескольких устройствах?</b>\n\n"
"— Да, Вы можете использовать VPN на 5 устройствах одновременно.\n\n"
"<b>2. Как подключить VPN на другом устройстве?</b>\n\n"
"— На другом устройстве нажмите Личный кабинет в главном меню, "
"затем нажмите Подключить VPN и следуйте инструкциям.\n\n"
"<b>3. Как пополнить баланс?</b>\n\n"
"— Нажмите Личный кабинет в главном меню, "
"затем нажмите Пополнить баланс и следуйте инструкциям.\n\n"
"<b>4. Что будет, если закончится баланс?</b>\n\n"
"— VPN просто перестанет работать, чтобы возобновить работу, пополните баланс.\n\n"
"<b>5. Моего вопроса тут нет, как написать поддержке?</b>\n\n"
"— Напишите поддержке, используя кнопку ниже, затем перешлите сообщение из кнопки Личный кабинет и опишите проблему."
)