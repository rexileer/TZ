from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.cart_dictionary import cart_dict


def get_cart_keyboard(user_id: int) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text="$ Заказать", callback_data="order_cart")],]
    
    if user_id in cart_dict:
        for product_id, quantity in cart_dict[user_id].items():
            buttons.append([
                InlineKeyboardButton(
                    text=f"❌ {product_id} ({quantity} шт.)",
                    callback_data=f"remove_from_cart_{product_id}"
                )
            ])

    buttons.append([InlineKeyboardButton(text="🧹 Очистить корзину", callback_data="clear_cart")],)
    buttons.append([InlineKeyboardButton(text="⬅️ Вернуться в каталог", callback_data="back_to_categories")],)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
