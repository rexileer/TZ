from django.contrib import admin
from .models import Order, OrderItem, ShippingDetails
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'created_at', 'total_price', 'status')
    inlines = [OrderItemInline]
    search_fields = ('user_id',)
    
class ShippingDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'address', 'phone_number', 'status')
    list_filter = ('status',)
    search_fields = ('order__id', 'address')

# Регистрируем модели в админке
admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingDetails, ShippingDetailsAdmin)
