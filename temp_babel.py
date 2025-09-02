from babel import Locale

# Получаем все доступные локали
all_locales = Locale.list_locales()

# Выводим коды локалей
for locale in sorted(all_locales, key=str):
    print(locale)

# Можно также получить список кодов
locale_codes = [str(locale) for locale in all_locales]
print(locale_codes)
