from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_subcategories_keyboard(category_id: int):
    subcategories = {
        1: [{"id": 10, "name": "Phones"}, {"id": 11, "name": "Laptops"}],
        2: [{"id": 20, "name": "Men"}, {"id": 21, "name": "Women"}],
    }

    buttons = [
        [InlineKeyboardButton(text=sub["name"], callback_data=f"subcategory_{sub['id']}")]
        for sub in subcategories.get(category_id, [])
    ]

    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_categories")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)