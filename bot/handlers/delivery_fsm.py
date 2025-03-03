from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from services.order_to_excel import add_order_to_excel
from services.cart_service import get_user_cart, clear_cart
from services.orders_service import create_order
from services.payment_service import create_payment, check_payment_status

import logging
logger = logging.getLogger(__name__)

router = Router()

class DeliveryState(StatesGroup):
    waiting_for_delivery_data = State()  # Ожидаем ввода данных для доставки

@router.callback_query(F.data == "delivery")
async def delivery_method_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    logger.info(f"User {user_id} triggered the delivery callback.")
    
    cart_products = await get_user_cart(user_id)
    if not cart_products:
        logger.warning(f"User {user_id} attempted to order, but the cart is empty.")
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
        text += f"{product.name} x{quantity} - ₽{price}\n"

    text += f"\n💰 Итоговая сумма: ₽{total_price}"

    # Сохраняем данные в FSMContext
    await state.update_data(total_price=total_price, cart_products=cart_products)

    # Запрашиваем данные для доставки
    logger.info(f"Total price for user {user_id} is ₽{total_price}. Requesting delivery data.")
    await callback.message.answer(text)
    await callback.message.answer("📝 Пожалуйста, введите данные для доставки (адрес, телефон и т.д.)")

    # Устанавливаем состояние
    await state.set_state(DeliveryState.waiting_for_delivery_data)
    await callback.answer()


@router.message(StateFilter(DeliveryState.waiting_for_delivery_data))
async def process_delivery_data(message: Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        total_price = state_data.get("total_price")

        if not total_price:
            logger.error(f"Total price not found in FSM state for user {message.from_user.id}.")
            await message.answer("Ошибка: не удалось получить сумму заказа.")
            return

        delivery_data = message.text
        await state.update_data(delivery_data=delivery_data)

        # Создаем платеж в YooKassa
        logger.info(f"Creating payment for user {message.from_user.id} with total price ₽{total_price}.")
        payment_id, payment_url = await create_payment(
            user_id=message.from_user.id, amount=total_price
        )
        

        if not payment_id:
            logger.error(f"Failed to create payment for user {message.from_user.id}.")
            await message.answer("❌ Ошибка при создании платежа.")
            return

        # Сохраняем payment_id в FSMContext
        await state.update_data(payment_id=payment_id)

        # Отправляем пользователю ссылку на оплату
        pay_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
                [InlineKeyboardButton(text="🔄 Проверить оплату", callback_data="check_payment")]
            ]
        )

        logger.info(f"Payment created for user {message.from_user.id}, sending payment link.")
        await message.answer(
            f"💰 Итоговая сумма: {total_price} ₽\n\n"
            "Для завершения заказа, пожалуйста, оплатите его.\n"
            "После оплаты нажмите 'Проверить оплату'.",
            reply_markup=pay_markup
        )

    except Exception as e:
        logger.error(f"Error in process_delivery_data for user {message.from_user.id}: {e}")
        await message.answer("❌ Произошла ошибка при обработке заказа.")


@router.callback_query(F.data == "check_payment")
async def check_payment_callback(callback: CallbackQuery, state: FSMContext):
    """Пользователь нажимает кнопку "Проверить оплату"""
    try:
        state_data = await state.get_data()
        payment_id = state_data.get("payment_id")

        if not payment_id:
            logger.warning(f"Payment ID not found for user {callback.from_user.id}.")
            await callback.message.answer("Ошибка: не найден идентификатор платежа.")
            return

        status = await check_payment_status(payment_id)

        if status == "succeeded":
            user_id = callback.from_user.id
            total_price = state_data.get("total_price")
            delivery_data = state_data.get("delivery_data")

            # Создаем заказ
            logger.info(f"Payment succeeded for user {user_id}, creating order.")
            order = await create_order(user_id, total_price, delivery_data)

            if order:
                logger.info(f"Order {order.id} created for user {user_id}, adding to Excel.")
                await add_order_to_excel({
                    "order_id": order.id,
                    "user_id": user_id,
                    "total_price": total_price,
                    "delivery_data": delivery_data,
                    "date": order.created_at
                })
                
                # Очищаем корзину
                await clear_cart(user_id)
                logger.info(f"Order {order.id} successfully completed for user {user_id}. Cart cleared.")
                await callback.message.answer("✅ Оплата прошла успешно! Ваш заказ оформлен. 🚀")
            else:
                logger.error(f"Failed to create order for user {user_id}.")
                await callback.message.answer("❌ Ошибка при создании заказа.")

            await state.clear()
        else:
            logger.warning(f"Payment for user {callback.from_user.id} not found or not confirmed.")
            await callback.message.answer("❌ Оплата не найдена или не подтверждена. Попробуйте позже.")

        await callback.answer()

    except Exception as e:
        logger.error(f"Error in check_payment_callback for user {callback.from_user.id}: {e}")
        await callback.message.answer("❌ Ошибка при проверке оплаты.")
