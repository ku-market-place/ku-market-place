"""Module contains the Order model."""
from django.db import models
from .customer import Customer
from .order_item import OrderItem


class Order(models.Model):
    """Class for order table."""

    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_item_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    total_amount = models.IntegerField(default=0)
