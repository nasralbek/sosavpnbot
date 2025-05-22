from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.utils.i18n import I18n

class ReplyButtonFilter(Filter):
    def __init__(self, button_key: str):
        self.button_key = button_key

    async def __call__(self, message: Message, i18n: I18n) -> bool:
        translated_text = i18n.gettext(self.button_key)  # Получаем перевод
        return message.text == translated_text