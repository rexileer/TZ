from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello")