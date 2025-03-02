from asgiref.sync import sync_to_async
from products.models import Category

@sync_to_async
def get_categories_from_db():
    return list(Category.objects.all()) 
