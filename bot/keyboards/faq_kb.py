from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.faq_service import get_faq_questions_from_db


async def get_faq_keyboard():
    faq_entries = await get_faq_questions_from_db()

    buttons = [
        [InlineKeyboardButton(text=faq.question, callback_data=f"faq_{faq.id}")]
        for faq in faq_entries
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
