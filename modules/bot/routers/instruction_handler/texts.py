from modules.bot.utils.navigation import NavInstruction

instructions_text = ('иструкция')

how_ios = (
"📱 <b>Инструкция для iOS</b>:\n"
"1. Установи V2Box из App Store.\n"
"2. Открой приложение, перейди в Configs и нажми “+”.\n"
"3. Скопируй ключ, выданный в боте, и выбери “Импорт из текста”.\n"
"4. Выбери добавленный ключ нажатием на него.\n"
"5. Нажми “Подключиться”.\n"
"<a href='%s'>%s</a>"
)

how_android = (
"🤖 <b>Инструкция для Android</b>:\n"
"1. Установи Hiddify из Google Play или с сайта hiddify.com.\n"
"2. Открой приложение и нажми “+”.\n"
"3. Выбери “Импорт из текста”.\n"
"4. Вставь ключ и нажми “Сохранить”.\n"
"5. Нажми “Старт” для подключения.\n"
"<a href='%s'>%s</a>"
)

how_windows =   (
"🪟 <b>Инструкция для Windows</b>:\n"
"1. Скачай Hiddify с сайта hiddify.com.\n"
"2. Установи и открой программу.\n"
"3. Нажми “Импорт → Из текста”.\n"
"4. Вставь ключ и нажми “Импортировать”.\n"
"5. Нажми “Подключиться”.\n"
"<a href='%s'>%s</a>"
)

how_macos = (
"💻 <b>Инструкция для MacOS</b>:\n"
"1. Установи Hiddify с сайта hiddify.com.\n"
"2. Открой и нажми “+”.\n"
"3. Выбери “Импорт из текста”.\n"
"4. Вставь ключ и нажми “Добавить”.\n"
"5. Нажми “Старт” для подключения.\n"
"<a href='%s'>%s</a>"
)


how_to_dict = {
NavInstruction.ANDROID : how_android,
NavInstruction.MAC     : how_macos,
NavInstruction.IOS     : how_ios,
NavInstruction.WIDNOWS : how_windows,
}