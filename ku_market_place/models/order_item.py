"""Module contains the OrderItem model."""
from django.db import models
from .product import Product


class OrderItem(models.Model):
    """Class for order item table."""

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
