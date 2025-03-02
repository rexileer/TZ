from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.cart_service import get_user_cart

async def get_cart_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Создает инлайн-клавиатуру для корзины, загружая данные из базы."""
    cart_products = await get_user_cart(user_id)
    buttons = []

    if cart_products:
        for cart_product in cart_products:
            product = cart_product.product
            quantity = cart_product.quantity

            buttons.append([
                InlineKeyboardButton(
                    text=f"❌ {product.name} ({quantity} шт.)",
                    callback_data=f"remove_from_cart_{product.id}"
                )
            ])

        buttons.append([InlineKeyboardButton(text="💰 Заказать", callback_data="order_cart")])
        buttons.append([InlineKeyboardButton(text="🧹 Очистить корзину", callback_data="clear_cart")])
    else:
        buttons.append([InlineKeyboardButton(text="🛍 Перейти в каталог", callback_data="back_to_categories")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
