from django.db import models
from django.contrib.auth.models import User

from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
    ]
    
    user_id = models.BigIntegerField()  # Telegram user_id
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Общая сумма заказа
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')  # Статус заказа
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    delivery_data = models.TextField()
    
    def __str__(self):
        return f"Order #{self.id} by {self.user_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Связь с заказом
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Продукт
    quantity = models.PositiveIntegerField()  # Количество товара
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Цена за единицу товара
    
    def save(self, *args, **kwargs):
        if not self.price:  # Если цена не указана
            self.price = self.product.price * self.quantity # Автоматически взять цену из продукта
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

class ShippingDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # Связь с заказом
    address = models.TextField()  # Адрес доставки
    phone_number = models.CharField(max_length=15)  # Номер телефона
    status = models.CharField(max_length=20, default="pending")  # Статус доставки (например, "в ожидании", "доставляется")
    
    def __str__(self):
        return f"Shipping for Order #{self.order.id} to {self.address}"
