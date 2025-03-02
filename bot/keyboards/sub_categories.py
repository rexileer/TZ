from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.subcategories_service import get_subcategories_from_db


async def get_subcategories_keyboard(category_id: int):
    subcategories = await get_subcategories_from_db(category_id)

    buttons = [
        [InlineKeyboardButton(text=subcategory.name, callback_data=f"subcategory_{subcategory.id}")]
        for subcategory in subcategories
    ]

    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_categories")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
