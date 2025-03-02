from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from handlers.cart_dictionary import cart_dict
from handlers.catalog import get_product_details
from keyboards.cart_kb import cart_keyboard

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

    keyboard = cart_keyboard

    await message.answer(text, reply_markup=keyboard)



@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    product_id = int(callback.data.split("_")[3])

    if user_id not in cart_dict:
        cart_dict[user_id] = {}

    if product_id in cart_dict[user_id]:
        cart_dict[user_id][product_id] += 1
    else:
        cart_dict[user_id][product_id] = 1

    await callback.answer("✅ Товар добавлен в корзину!")
    
@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in cart_dict:
        cart_dict[user_id].clear()

    await callback.message.edit_text("🛒 Корзина очищена.")
    await callback.answer()
