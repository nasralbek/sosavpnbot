import os
import requests
from time import sleep

# Конфигурация
BOT_TOKEN = "7518561707:AAGhfU3wyVR2Sf30u3Sk1e2Mxteb8UbBI-k"  # Замените на токен вашего бота
PHOTO_PATH = "modules/bot/photo.jpeg"  # Путь к изображению для рассылки
USERS_FILE = "modules/bot/users.txt"  # Файл с user_id пользователей (каждый с новой строки)
DELAY = 0.5  # Задержка между сообщениями (в секундах)

# Текст сообщения
MESSAGE_TEXT = """<b>⚡️ Я Ваш личный бот и диалоговый помощник Sosa Spy!</b>

• Уведомление о редактировании сообщения собеседником.
• Уведомление об удалении сообщения собеседником.
• Скачивание медиа с таймером.
• Анонимный просмотр/скачивание историй.

🔴 Бот работает даже, когда вы оффлайн.

<a href="t.me/sosaspybot"><b>Подключить Sosa Spy</b></a>"""

def send_photo_with_caption(chat_id, photo_path, caption, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(photo_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': chat_id, 'caption': caption, 'parse_mode': parse_mode}
        response = requests.post(url, files=files, data=data)
    return response.json()

def main():
    # Проверяем наличие файла с фото
    if not os.path.exists(PHOTO_PATH):
        print(f"Ошибка: Файл с фото {PHOTO_PATH} не найден!")
        return
    
    # Читаем user_id из файла
    try:
        with open(USERS_FILE, 'r') as file:
            user_ids = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Ошибка: Файл с пользователями {USERS_FILE} не найден!")
        return
    
    if not user_ids:
        print("Файл users.txt пуст или содержит некорректные данные!")
        return
    
    print(f"Начинаю рассылку для {len(user_ids)} пользователей...")
    
    for i, user_id in enumerate(user_ids, 1):
        try:
            print(f"Отправляю сообщение пользователю {user_id} ({i}/{len(user_ids)})...")
            result = send_photo_with_caption(user_id, PHOTO_PATH, MESSAGE_TEXT)
            
            if not result.get('ok'):
                print(f"Ошибка при отправке для {user_id}: {result.get('description')}")
            
            sleep(DELAY)  # Задержка между сообщениями
            
        except Exception as e:
            print(f"Ошибка при отправке для {user_id}: {str(e)}")
    
    print("Рассылка завершена!")

if __name__ == "__main__":
    main()