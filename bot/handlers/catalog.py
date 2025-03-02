from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import categories, sub_categories, products_kb
from services.products_service import get_product_details_from_db
from services.subcategories_service import get_category_by_subcategory

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
    if callback.message.text:
        await callback.message.edit_text("-------Choose a category-------", reply_markup=keyboard)
    else:
        
        await callback.message.answer("-------Choose a category-------", reply_markup=keyboard)
    
    await callback.answer()

@router.callback_query(F.data.startswith("subcategory_"))
async def show_products(callback: CallbackQuery):
    subcategory_id = int(callback.data.split("_")[1])
    keyboard = await products_kb.get_products_keyboard(subcategory_id)
    await callback.message.edit_text("Choose a product:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("product_"))
async def show_product_details(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    product = await get_product_details_from_db(product_id)

    if product:
        keyboard = products_kb.get_quantity_keyboard(product_id)
        await callback.message.answer_photo(
            photo=product.image_url,
            caption=f"**{product.name}**\n💵 Price: ${product.price}\n📌 {product.description}",
            reply_markup=keyboard
        )
    else:
        await callback.message.answer("Product not found.")
    await callback.answer()


@router.callback_query(F.data == "back_to_subcategories")
async def back_to_subcategories(callback: CallbackQuery):
    subcategory_id = int(callback.message.reply_markup.inline_keyboard[0][0].callback_data.split("_")[1])
    category_id = await get_category_by_subcategory(subcategory_id)
    
    keyboard = await sub_categories.get_subcategories_keyboard(category_id)
    await callback.message.edit_text("Choose a subcategory:", reply_markup=keyboard)
    await callback.answer()
