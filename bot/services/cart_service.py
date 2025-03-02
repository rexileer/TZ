from asgiref.sync import sync_to_async
from products.models import Cart, CartProduct, Product
from django.core.exceptions import ObjectDoesNotExist

@sync_to_async
def get_user_cart(user_id):
    try:
        cart = Cart.objects.get(user_id=user_id)
        cart_products = CartProduct.objects.filter(cart=cart)
        
        return cart_products
    except ObjectDoesNotExist:
        return [] 


@sync_to_async
def add_to_cart(user_id, product_id, quantity):
    try:
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        product = Product.objects.get(id=product_id)

        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_product.quantity += quantity
            
            cart_product.save()
        else:
            cart_product.quantity = quantity
            
            cart_product.save()
    except Product.DoesNotExist:
        return None


@sync_to_async
def remove_from_cart(user_id, product_id):
    try:
        cart = Cart.objects.get(user_id=user_id)
        product = Product.objects.get(id=product_id)
        cart_product = CartProduct.objects.get(cart=cart, product=product)

        cart_product.delete()
        
        return True
    except CartProduct.DoesNotExist:
        return False


@sync_to_async
def clear_cart(user_id):
    try:
        cart = Cart.objects.get(user_id=user_id)
        
        cart.cart_products.all().delete()
        
        return True
    except Cart.DoesNotExist:
        return False
