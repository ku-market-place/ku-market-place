from django.db import models
from .product import Product


class OrderItem(models.Model):

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)
