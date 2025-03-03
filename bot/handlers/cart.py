from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from services.cart_service import get_user_cart, add_to_cart, remove_from_cart, clear_cart
from services.products_service import get_product_details_from_db
from keyboards.cart_kb import get_cart_keyboard
from keyboards.products_kb import get_product_to_cart_keyboard
from keyboards import reply

router = Router()


@router.message(F.text == "Cart")
async def show_cart(message: Message):
    """Отображение корзины пользователя"""
    user_id = message.from_user.id
    cart_products = await get_user_cart(user_id)
    
    if not cart_products:
        await message.answer("🛒 Ваша корзина пуста.")
        return
    
    text = "🛒 **Ваша корзина:**\n"
    total_price = 0

    for cart_product in cart_products:
        product = cart_product.product
        quantity = cart_product.quantity
        price = product.price * quantity
        total_price += price
        text += f"🛍 **{product.name}** x{quantity} - ₽{price}\n"

    text += f"\n💰 **Итоговая сумма:** ₽{total_price}"

    keyboard = await get_cart_keyboard(user_id)
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "clear_cart")
async def clear_cart_callback(callback: CallbackQuery):
    """Очистка корзины"""
    user_id = callback.from_user.id
    await clear_cart(user_id)
    await callback.message.edit_text("🛒 Корзина очищена.")
    await callback.answer()


@router.callback_query(F.data.startswith("set_quantity_"))
async def set_quantity_callback(callback: CallbackQuery):
    """Установка количества товара перед добавлением в корзину"""
    product_id, quantity = map(int, callback.data.split("_")[2:])

    product = await get_product_details_from_db(product_id)
    if not product:
        await callback.message.answer("❌ Товар не найден.")
        return

    await callback.message.answer(
        f"Вы желаете добавить {quantity} шт. товара **{product.name}** в корзину?",
        reply_markup=get_product_to_cart_keyboard(product_id, quantity)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart_callback(callback: CallbackQuery):
    """Добавление товара в корзину"""
    product_id, quantity = map(int, callback.data.split("_")[3:])
    user_id = callback.from_user.id

    product = await get_product_details_from_db(product_id)
    if not product:
        await callback.message.answer("❌ Товар не найден.")
        return

    await add_to_cart(user_id, product_id, quantity)

    await callback.message.delete()

    await callback.message.answer(f"✅ Добавлено {quantity} шт. товара **{product.name}** в корзину.", reply_markup=reply.main)
    await callback.answer()


@router.callback_query(F.data.startswith("remove_from_cart_"))
async def remove_from_cart_callback(callback: CallbackQuery):
    """Удаление товара из корзины"""
    product_id = int(callback.data.split("_")[3])
    user_id = callback.from_user.id

    product = await get_product_details_from_db(product_id)
    if not product:
        await callback.message.answer("❌ Товар не найден.")
        return

    await remove_from_cart(user_id, product_id)
    
    keyboard = await get_cart_keyboard(user_id)
    await callback.message.edit_text(
        text="🛒 Ваша корзина обновлена.",
        reply_markup=keyboard
    )
    await callback.answer(f"❌ {product.name} удален из корзины.")
