from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_products_keyboard(subcategory_id: int):
    products = {
        10: [
            {"id": 100, "name": "iPhone 15", "price": 1000},
            {"id": 101, "name": "Samsung S24", "price": 900},
        ],
        11: [
            {"id": 102, "name": "MacBook Pro", "price": 2500},
            {"id": 103, "name": "Asus ROG", "price": 2000},
        ],
        20: [
            {"id": 104, "name": "Men's Jacket", "price": 100},
            {"id": 105, "name": "Men's Shoes", "price": 150},
        ],
        21: [
            {"id": 106, "name": "Women's Dress", "price": 120},
            {"id": 107, "name": "Women's Shoes", "price": 130},
        ],
    }

    buttons = [
        [InlineKeyboardButton(text=f"{prod['name']} - ${prod['price']}", callback_data=f"product_{prod['id']}")]
        for prod in products.get(subcategory_id, [])
    ]

    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_subcategories")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_product_to_cart_keyboard(product_id: int, quantity: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Add to Cart", callback_data=f"add_to_cart_{product_id}_{quantity}")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_subcategories")]
    ])


def get_quantity_keyboard(product_id: int) -> InlineKeyboardMarkup:
    quantities = [
        [InlineKeyboardButton(text=str(i), callback_data=f"set_quantity_{product_id}_{i}")]
        for i in range(1, 6)
    ]
    return InlineKeyboardMarkup(inline_keyboard=quantities)