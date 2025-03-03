from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_delivery_keyboard(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🚚 Продолжить и ввести данные для доставки", callback_data="delivery"),
        InlineKeyboardButton(text="🛍 Перейти в каталог", callback_data="back_to_categories")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)