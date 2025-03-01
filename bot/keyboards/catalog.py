from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CATEGORIES_PER_PAGE = 5

# Функция для создания клавиатуры с категориями
async def get_categories_keyboard(page: int = 1):
    categories = await get_categories_from_db()
    total_pages = (len(categories) - 1) // CATEGORIES_PER_PAGE + 1
    start_idx = (page - 1) * CATEGORIES_PER_PAGE
    end_idx = start_idx + CATEGORIES_PER_PAGE
    page_categories = categories[start_idx:end_idx]

    buttons = [[InlineKeyboardButton(text=category["name"], callback_data=f"category_{category['id']}")]
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

# Имитация получения категорий из базы данных
async def get_categories_from_db():
    return [
        {"id": 1, "name": "Electronics"},
        {"id": 2, "name": "Clothing"},
        {"id": 3, "name": "Books"},
        {"id": 4, "name": "Toys"},
        {"id": 5, "name": "Beauty"},
        {"id": 6, "name": "Furniture"},
        {"id": 7, "name": "Sports"},
        {"id": 8, "name": "Electronics"},
        {"id": 9, "name": "Clothing"},
        {"id": 10, "name": "Books"},
        {"id": 11, "name": "Toys"},
        {"id": 12, "name": "Beauty"},
        {"id": 13, "name": "Furniture"},
        {"id": 14, "name": "Sports"},
        {"id": 15, "name": "Electronics"},
        {"id": 16, "name": "Clothing"},
        {"id": 17, "name": "Books"},
        {"id": 18, "name": "Toys"},
        {"id": 19, "name": "Beauty"},
        {"id": 20, "name": "Furniture"},
        {"id": 21, "name": "Sports"},
    ]

# Клавиатура подкатегорий
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

# Клавиатура товаров
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

# Клавиатура продукта
def get_product_keyboard(product_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Add to Cart", callback_data=f"add_to_cart_{product_id}")],
    ])
