from django.contrib import admin
from .models import Cart, CartProduct, Product, Category, SubCategory, FAQ

# Регистрация модели категории
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    ordering = ('created_at',)

# Регистрация модели подкатегории
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'created_at')
    ordering = ('created_at',)

# Регистрация модели товара
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'price', 'created_at')
    ordering = ('created_at',)

class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_id',)
    inlines = [CartProductInline]

@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')