from asgiref.sync import sync_to_async
from products.models import SubCategory


@sync_to_async
def get_subcategories_from_db(category_id):
    return list(SubCategory.objects.filter(category_id=category_id))

@sync_to_async
def get_category_by_subcategory(subcategory_id):
    subcategory = SubCategory.objects.filter(id=subcategory_id).first()
    return subcategory.category.id if subcategory else None