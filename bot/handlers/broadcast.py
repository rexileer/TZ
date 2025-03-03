from aiogram import Router, F
from aiogram.types import Message
from services.broadcast_service import get_broadcast

router = Router()

@router.message(F.text == "Broadcast")
async def show_broadcast(message: Message):
    broadcast = await get_broadcast()
    if broadcast:
        await message.answer(text=f"Рассылка: {broadcast.message}")
    else:
        await message.answer(text="Нет активных рассылок.")