from django.db import models


class Basket(models.Model):
    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="basket_products")
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Корзина {self.author.username} - Продукт {self.product.title} - {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('processed', 'Обработано'),
        ('shipped', 'Отправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Отменено'),
    )

    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="orders")
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.author.username}"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.title} ({self.quantity}) in Order {self.order.id}'


