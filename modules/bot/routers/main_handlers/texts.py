from math import ceil
import time
from datetime import date

def gen_reflink(botname,user_id):
    return f"https://t.me/{botname}?start={user_id}"

def profile_text(user,botname):
    user_id  = user.user_id
    refs     = user.referrals    

    refilnk = gen_reflink(botname,user_id)

    return (
        #f"Ваш id: <b>{user_id}</b>\n"
        f"Приглашено: <b>{refs} чел.</b>\n\n"
        f"👥 За каждого приглашенного друга по реферальной ссылке ты получишь <b>50₽ (15 дней)</b> на баланс, друг получит <b>100₽ (30 дней)</b>.\n\n"
        f"🔗 <b>Твоя реферальная ссылка:</b>\n{refilnk}\n"
    )

def connect_text(key,expiry_time):
    price = 3.33
    remaining_days = ceil((expiry_time - time.time()*1000)/1000/24/60/60)
    
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
        result_text+=f"⚙️ <b>Ваша подписка Sosa VPN:</b>\n"
        result_text+=f"├ Статус: <b>Активна ✅</b>\n"
        result_text+=f"├ Тариф: <b>3.3₽/день</b>\n"
        result_text+=f"└ Баланс: <b>{balance}₽ ({remaining_days} дней)</b>\n\n"
        result_text+=f"🗝 <b>Ваш ключ:</b> <blockquote><code>{key}</code></blockquote>\n\n"
        result_text+=f"<b>Для подключения к VPN используйте кнопку снизу.</b>"
    else:
        result_text+=f"⚙️ <b>Ваша подписка Sosa VPN:</b>\n"
        result_text+=f"├ Статус: <b>Неактивна ⚠️</b>\n"
        result_text+=f"├ Тариф: <b>3.3₽/день</b>\n"
        result_text+=f"└ Баланс: <b>0₽ (0 дней)</b>\n\n"
        result_text+=f"🗝 <b>Ваш ключ:</b> <blockquote><code>{key}</code></blockquote>\n\n"
        result_text+="<b>Для активации подписки пополните баланс или пригласите друга.</b>"
    return result_text

information_text = (
"Sosa VPN использует протокол с открытым исходным кодом, который имеет наилучшую производительность, "
"по сравнению с другими. Все наши сервера оснащены каналом 1 гбит/с.\n\n"
"Журнал логов удаляется с наших серверов моментально, мы не храним историю посещений, в отличии от многих "
"бесплатных сервисов. Мы не собираем и не продаём какие либо данные о Вас.\n\n"
"Для выдачи доступа к VPN используется Telegram, в связи с этим нас не возможно заблокировать или удалить "
"из App Store и других площадок."
)