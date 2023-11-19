from django.db import models
from .product import Product


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total_amount = models.FloatField(default=0)

    def __str__(self):
        return self.product.productDisplayName
