from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from services import client_service
from keyboards import reply

import logging
logger = logging.getLogger(__name__)

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    logger.info(f"Received /start command from {message.from_user.id}")  
    await client_service.add_client_to_db(message.from_user)
    await message.answer("Welcome to the AnyTechShop bot! Please choose an action from the menu.", reply_markup=reply.main)
