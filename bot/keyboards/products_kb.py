from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.products_service import get_products_from_db


async def get_products_keyboard(subcategory_id: int):
    products = await get_products_from_db(subcategory_id)

    buttons = [
        [InlineKeyboardButton(text=f"{product.name} - ₽{product.price}", callback_data=f"product_{product.id}")]
        for product in products
    ]

    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_subcategories")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_product_to_cart_keyboard(product_id: int, quantity: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Add to Cart", callback_data=f"add_to_cart_{product_id}_{quantity}")],
        [InlineKeyboardButton(text="⬅️ Перейти в каталог", callback_data="back_to_categories")]
    ])


def get_quantity_keyboard(product_id: int) -> InlineKeyboardMarkup:
    quantities = [
        [InlineKeyboardButton(text=str(i), callback_data=f"set_quantity_{product_id}_{i}")]
        for i in range(1, 6)
    ]
    quantities.append([InlineKeyboardButton(text="⬅️ Перейти в каталог", callback_data="back_to_categories")])
    return InlineKeyboardMarkup(inline_keyboard=quantities)
