
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cart_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🧹 Очистить корзину", callback_data="clear_cart")],
    [InlineKeyboardButton(text="⬅️ Вернуться в каталог", callback_data="back_to_categories")]
])