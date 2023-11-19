from django.db import models
from .customer import Customer
from .order_item import OrderItem


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        SHIPPING = 'Shipping', 'Shipping'
        DELIVERY = 'Delivery', 'Delivery'
        COMPLETE = 'Complete', 'Complete'
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_item_id = models.ManyToManyField(OrderItem)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.SHIPPING
    )
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
