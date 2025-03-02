from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards import reply

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Welcome to the AnyTechShop bot! Please choose an action from the menu.", reply_markup=reply.main)
