from configs.main_config import REFERRAL_PROGRAMM_CONFIG
from modules.bot.callbacks import how_to_callbacks
from math import ceil
import time
from datetime import date

how_ios = (
"📱 <b>Инструкция для iOS</b>:\n"
"1. Установи V2Box из App Store.\n"
"2. Открой приложение, перейди в Configs и нажми “+”.\n"
"3. Скопируй ключ, выданный в боте, и выбери “Импорт из текста”.\n"
"4. Выбери добавленный ключ нажатием на него.\n"
"5. Нажми “Подключиться”."
)

how_android = (
"🤖 <b>Инструкция для Android</b>:\n"
"1. Установи Hiddify из Google Play или с сайта hiddify.com.\n"
"2. Открой приложение и нажми “+”.\n"
"3. Выбери “Импорт из текста”.\n"
"4. Вставь ключ и нажми “Сохранить”.\n"
"5. Нажми “Старт” для подключения."
)

how_windows =   (
"🪟 <b>Инструкция для Windows</b>:\n"
"1. Скачай Hiddify с сайта hiddify.com.\n"
"2. Установи и открой программу.\n"
"3. Нажми “Импорт → Из текста”.\n"
"4. Вставь ключ и нажми “Импортировать”.\n"
"5. Нажми “Подключиться”."
)

how_macos = (
"💻 <b>Инструкция для MacOS</b>:\n"
"1. Установи Hiddify с сайта hiddify.com.\n"
"2. Открой и нажми “+”.\n"
"3. Выбери “Импорт из текста”.\n"
"4. Вставь ключ и нажми “Добавить”.\n"
"5. Нажми “Старт” для подключения."
)

how_to_dict = {
    how_to_callbacks.how_to_macos:how_macos,
    how_to_callbacks.how_to_windows:how_windows,
    how_to_callbacks.how_to_android:how_android,
    how_to_callbacks.how_to_ios:how_ios,
}

how_not_found = "❗ Инструкция не найдена."


info = (
"Sosa VPN использует протокол с открытым исходным кодом, который имеет наилучшую производительность, "
"по сравнению с другими. Все наши сервера оснащены каналом 1 гбит/с.\n\n"
"Журнал логов удаляется с наших серверов моментально, мы не храним историю посещений, в отличии от многих "
"бесплатных сервисов. Мы не собираем и не продаём какие либо данные о Вас.\n\n"
"Для выдачи доступа к VPN используется Telegram, в связи с этим нас не возможно заблокировать или удалить "
"из App Store и других площадок."
)

welcome_text = (
"Я Ваш личный бот и помощник Sosa VPN!\n\n"
"Я помогаю c обходом блокировок и защитой вашей конфиденциальности.\n\n"
"Для использования сервиса Вам не нужно нигде регистрироваться, просто оплатите подписку и начните пользоваться VPN.\n"
"Все происходит внутри Telegram.")

connect_vpn_message = (
"⚡️ Вы покупаете премиум подписку на Sosa VPN.\n\n"
"• До 5 устройств одновременно\n"
"• Без ограничений по скорости и трафику"
)
not_enough_money_text = "❌ Недостаточно средств на балансе."

choose_replenishment_method = 'Выберите способ оплаты'

notify_referrer = (
f"🎉 Новый пользователь зарегистрировался по твоей ссылке!\n"
f"Тебе начислено {REFERRAL_PROGRAMM_CONFIG.BONUS_TO_INVITER}₽."
)

notify_invited = (
    f"🎁 Добро пожаловать!\n"
    f"Тебе начислено {REFERRAL_PROGRAMM_CONFIG.BONUS_TO_INVITED}₽ за регистрацию по реферальной ссылке."
)

def gen_balance_text():
    return ("способы оплаты:\n\n\n" \
            "тарифы:\n\n\n")

def gen_connect_text(key,expiry_time):
    price = 3.33
    remaining_days = ceil((expiry_time - time.time()*1000)/1000/24/60/60)
    
    balance = ceil(remaining_days*price)
    expiry_date = date.fromtimestamp(expiry_time/1000)
    day = expiry_date.day
    month = expiry_date.month
    year = expiry_date.year
    expiry_date_text = f"{day}.{0 if month <10 else ""}{month}.{year}"
    #TODO FIX
    #TODO: add balance (with days)

    result_text =""
    if remaining_days>0:
        result_text+=f"баланс <b>{balance}</b> рубелей\n"
        result_text+=f"осталось <b>{remaining_days}</b> дней\n"
        result_text+=f"действует до <b>{expiry_date_text}</b>\n\n"
    else:
        result_text+="не поднлючено, пополните баланс или пригласите друга\n\n"


    result_text += f"ваш ключ:\n<code>{key}</code>\n"

    
    return result_text
           


def profile_text(refs,user_id,botname):
    #TODO: remove balance
    return (
        f"Ваш id: <b>{user_id}</b>\n"
        f"Приглашено: <b>{refs} чел.</b>\n\n"
        f"🔗 За каждого приглашенного друга ты получаешь 50₽ на баланс, друг получает 100₽.\n\n"
        f"👥 <b>Твоя реферальная ссылка:</b>\n{gen_reflink(botname,user_id)}\n"
    )

instructions_text = 'Выберите ваше устройство'

def gen_reflink(botname,user_id):
    return f"https://t.me/{botname}?start={user_id}"


    
def gen_want_to_purshare_balance(days,cost):
    return (
        f"Вы собираетесь купить VPN на {days} дней.\n"\
    	f"С вашего баланса будет списано {cost}₽."
    )

def gen_want_to_purshare_yokassa(days,cost,url):
    return 	(
        f"Вы собираетесь купить VPN на {days} дней.\n"\
        f"Стоимость: {cost}\n" \
        f"Ссылка для оплаты vpn:\n"\
        f"{url}"
        )

