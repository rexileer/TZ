from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards import reply

from handlers.cart_dictionary import cart_dict

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    if user_id not in cart_dict:
        cart_dict[user_id] = {}  # Создаем пустую корзину
        
    await message.answer("Welcome to the AnyTechShop bot! Please choose an action from the menu.", reply_markup=reply.main)
