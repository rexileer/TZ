from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Cart(models.Model):
    user_id = models.BigIntegerField()
    products = models.ManyToManyField(Product, through='CartProduct')
    
    def __str__(self):
        return f"Cart for user {self.user_id}"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_products", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_products", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart product {self.product.name} - Quantity: {self.quantity}"

    class Meta:
        verbose_name = "CartProduct"
        verbose_name_plural = "CartProducts"


class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"
