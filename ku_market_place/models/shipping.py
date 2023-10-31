from django.db import models
from .order import Order
from .customer import Customer


class Shipping(models.Model):

    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
