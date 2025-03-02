from asgiref.sync import sync_to_async
from products.models import Product


@sync_to_async
def get_products_from_db(subcategory_id):
    return list(Product.objects.filter(subcategory_id=subcategory_id))

@sync_to_async
def get_product_details_from_db(product_id):
    return Product.objects.filter(id=product_id).first()