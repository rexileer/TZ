from django.contrib import admin
from .models import Order, OrderItem, Client


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'created_at', 'total_price', 'status')
    inlines = [OrderItemInline]
    search_fields = ('user_id',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'username', 'first_name', 'last_name', 'email', 'subscribed', 'registration_date')
    list_filter = ('subscribed',)
    search_fields = ('first_name', 'last_name', 'email')

# Регистрируем модели в админке
admin.site.register(Order, OrderAdmin)
admin.site.register(Client, ClientAdmin)
