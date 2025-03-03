from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from services.cart_service import get_user_cart
from services.orders_service import create_order

router = Router()

class DeliveryState(StatesGroup):
    waiting_for_delivery_data = State()  # Ожидаем ввода данных для доставки

@router.callback_query(F.data == "delivery")
async def delivery_method_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cart_products = await get_user_cart(user_id)

    if not cart_products:
        await callback.message.answer("🛒 Ваша корзина пуста. Добавьте товары в корзину.")
        return

    # Генерируем текст для заказа
    text = "📝 Оформление заказа:\n"
    total_price = 0
    for cart_product in cart_products:
        product = cart_product.product
        quantity = cart_product.quantity
        price = product.price * quantity
        total_price += price
        text += f"{product.name} x{quantity} - ${price}\n"

    text += f"\n💰 Итоговая сумма: ${total_price}"

    # Сохраняем данные в FSMContext
    await state.update_data(total_price=total_price, cart_products=cart_products)

    # Запрашиваем данные для доставки
    await callback.message.answer(text)
    await callback.message.answer("📝 Пожалуйста, введите данные для доставки (адрес, телефон и т.д.)")

    # Устанавливаем состояние
    await state.set_state(DeliveryState.waiting_for_delivery_data)
    await callback.answer()

@router.message(StateFilter(DeliveryState.waiting_for_delivery_data))
async def process_delivery_data(message: Message, state: FSMContext):
    try:
        print("Функция process_delivery_data вызвана")
        state_data = await state.get_data()
        total_price = state_data.get("total_price")
        
        if not total_price:
            await message.answer("Ошибка: не удалось получить сумму заказа.")
            return
        
        delivery_data = message.text
        print(f"Создаём заказ: user_id={message.from_user.id}, total_price={total_price}, delivery_data={delivery_data}")

        order = await create_order(
            user_id=message.from_user.id,
            total_price=total_price,
            delivery_data=delivery_data
        )

        if not order:
            await message.answer("❌ Ошибка при создании заказа.")
            return

        await message.answer(f"✅ Заказ оформлен! 🚀\nДоставка: {delivery_data}\nСумма: {total_price}$")

        await state.clear()

    except Exception as e:
        print(f"Ошибка в process_delivery_data: {e}")
        await message.answer("❌ Произошла ошибка при оформлении заказа.")
