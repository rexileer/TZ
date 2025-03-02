from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards import categories, sub_categories, products

router = Router()

@router.message(F.text == "Catalog")
async def show_categories(message: Message):
    keyboard = await categories.get_categories_keyboard(page=1)
    await message.answer("-------Choose a category-------", reply_markup=keyboard)

@router.callback_query(F.data.startswith("page_"))
async def paginate_categories(callback_query: CallbackQuery):
    page = int(callback_query.data.split("_")[1])
    keyboard = await categories.get_categories_keyboard(page=page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()

@router.callback_query(F.data.startswith("category_"))
async def show_subcategories(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    keyboard = await sub_categories.get_subcategories_keyboard(category_id)
    await callback.message.edit_text("Choose a subcategory:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    keyboard = await categories.get_categories_keyboard()
    await callback.message.edit_text("Choose a category:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("subcategory_"))
async def show_products(callback: CallbackQuery):
    subcategory_id = int(callback.data.split("_")[1])
    keyboard = await products.get_products_keyboard(subcategory_id)
    await callback.message.edit_text("Choose a product:", reply_markup=keyboard)
    await callback.answer()

async def get_product_details(product_id: int):
    product_details = {
        100: {"name": "iPhone 15", "price": 1000, "description": "Latest Apple iPhone", "photo": "https://hi-stores.ru/catalog/iphone/iphone-15/47488/#gallery-1"},
        101: {"name": "Samsung S24", "price": 900, "description": "Latest Samsung flagship", "photo": "https://example.com/s24.jpg"},
        102: {"name": "MacBook Pro", "price": 2500, "description": "Powerful laptop", "photo": "https://example.com/macbook.jpg"},
    }
    return product_details.get(product_id, None)

@router.callback_query(F.data.startswith("product_"))
async def show_product_details(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    product = await get_product_details(product_id)

    if product:
        keyboard = products.get_quantity_keyboard(product_id)
        await callback.message.answer_photo(
            photo=product["photo"], 
            caption=f"**{product['name']}**\n💵 Price: ${product['price']}\n📌 {product['description']}", 
            reply_markup=keyboard
        )
    else:
        await callback.message.answer("Product not found.")
    await callback.answer()

@router.callback_query(F.data == "back_to_subcategories")
async def back_to_subcategories(callback: CallbackQuery):
    category_id = 1  # Тут надо будет запоминать категорию, пока фиксированное значение
    keyboard = await sub_categories.get_subcategories_keyboard(category_id)
    await callback.message.edit_text("Choose a subcategory:", reply_markup=keyboard)
    await callback.answer()

