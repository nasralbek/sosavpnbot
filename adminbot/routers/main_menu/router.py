import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("start"))
async def main_menu(message:Message):
    await message.answer("Hello! This is the main menu.")
    
