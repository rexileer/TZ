from django.contrib import admin
from .models import Category, SubCategory, Product

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
