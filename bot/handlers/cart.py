from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from handlers.cart_dictionary import cart_dict
from handlers.catalog import get_product_details
from keyboards.cart_kb import get_cart_keyboard
from keyboards.products import get_product_to_cart_keyboard

router = Router()

@router.message(F.text == "Cart")
async def show_cart(message: Message):
    user_id = message.from_user.id
    if user_id not in cart_dict or not cart_dict[user_id]:
        await message.answer("🛒 Ваша корзина пуста.")
        return

    text = "🛒 Ваша корзина:\n"
    total_price = 0

    for product_id, quantity in cart_dict[user_id].items():
        product = await get_product_details(product_id)
        if product:
            price = product["price"] * quantity
            total_price += price
            text += f"{product['name']} x{quantity} - ${price}\n"

    text += f"\n💰 Итоговая сумма: ${total_price}"

    keyboard = get_cart_keyboard(user_id)

    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in cart_dict:
        cart_dict[user_id].clear()

    await callback.message.edit_text("🛒 Корзина очищена.")
    await callback.answer()

@router.callback_query(F.data.startswith("set_quantity_"))
async def set_quantity(callback: CallbackQuery):
    product_id, quantity = callback.data.split("_")[2:]
    product_id = int(product_id)
    quantity = int(quantity)

    await callback.message.answer(f"Вы желаете добавить {quantity} шт. товара {product_id} в корзину?", reply_markup=get_product_to_cart_keyboard(product_id, quantity)) # Заменить id на название товара
    
    await callback.answer()


@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery):
    product_id, quantity = callback.data.split("_")[3:]
    product_id = int(product_id)
    user_id = callback.from_user.id
    quantity = int(quantity)
    
    if user_id not in cart_dict:
        cart_dict[user_id] = {}
    
    if product_id in cart_dict[user_id]:
        cart_dict[user_id][product_id] += quantity
    else:
        cart_dict[user_id][product_id] = quantity

    await callback.message.delete()

    await callback.message.answer(f"✅ Добавлено {quantity} шт. товара {product_id} в корзину.") # Заменить id на название товара
    
    await callback.answer()

@router.callback_query(F.data.startswith("remove_from_cart_"))
async def remove_from_cart(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[3])

    if callback.from_user.id in cart_dict and product_id in cart_dict[callback.from_user.id]:
        del cart_dict[callback.from_user.id][product_id]
    
    await callback.message.edit_text(
        text="🛒 Ваша корзина обновлена.",
        reply_markup=get_cart_keyboard(callback.from_user.id)
    )
    await callback.answer("Товар удален из корзины.")
