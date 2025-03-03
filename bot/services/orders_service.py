from asgiref.sync import sync_to_async
from customers.models import Order, OrderItem
from products.models import Cart, CartProduct

@sync_to_async
def create_order(user_id, total_price, delivery_data):
    try:
        cart = Cart.objects.get(user_id=user_id)
        cart_products = CartProduct.objects.filter(cart=cart)

        if not cart_products.exists():
            return None  # Корзина пуста

        # Создаём заказ
        order = Order.objects.create(
            user_id=user_id,
            total_price=total_price,
            delivery_data=delivery_data,
            status="new"  # Новый заказ
        )

        # Создаём OrderItem для каждого товара в корзине
        for cart_product in cart_products:
            OrderItem.objects.create(
                order=order,
                product=cart_product.product,
                quantity=cart_product.quantity,
                price=cart_product.product.price * cart_product.quantity
            )

        # Очищаем корзину после оформления заказа
        cart_products.delete()

        return order
    except Exception as e:
        print(f"Ошибка при создании заказа: {e}")
        return None
