from aiogram.filters import Filter
from aiogram.types import CallbackQuery
from modules.bot.utils.navigation import NavInformation,NavConnect,NavInstruction

class InstructionFilter(Filter):
    def __init__(self):
        self.instruction_callbacks = [NavConnect.INSTRUCTIONS,NavInformation.INSTRUCTIONS]

    async def __call__(self, callback: CallbackQuery):
        return callback.data in self.instruction_callbacks
        
class HowToFilter(Filter):
    def __init__(self):
        self.start = NavInstruction.MAIN
    
    async def __call__(self, callback: CallbackQuery):
        return callback.data.startswith(self.start)