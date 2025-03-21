from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.categories_service import get_categories_from_db

CATEGORIES_PER_PAGE = 5


async def get_categories_keyboard(page: int = 1):
    categories = await get_categories_from_db()
    total_pages = (len(categories) - 1) // CATEGORIES_PER_PAGE + 1
    start_idx = (page - 1) * CATEGORIES_PER_PAGE
    end_idx = start_idx + CATEGORIES_PER_PAGE
    page_categories = categories[start_idx:end_idx]

    buttons = [[InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}")]
               for category in page_categories]

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️ Prev", callback_data=f"page_{page - 1}"))
    if page < total_pages:
        pagination_buttons.append(InlineKeyboardButton(text="Next ➡️", callback_data=f"page_{page + 1}"))

    if pagination_buttons:
        buttons.append(pagination_buttons)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
