from django.db import models
from django.contrib.auth.models import User


# ✅ Product model (ONLY ONE)
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    def __str__(self):
        return self.name


# ✅ Order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order {self.id}"


# ✅ OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)  # 🔥 FIXED
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"