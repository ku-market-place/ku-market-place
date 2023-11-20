from django.db import models
from .customer import Customer
from .order_item import OrderItem


class Order(models.Model):
    """Class for order table."""
    class OrderStatus(models.TextChoices):
        SHIPPING = 'Shipping', 'Shipping'
        DELIVERY = 'Delivery', 'Delivery'
        PREPARE = 'Prepare', 'Prepare'

    class Payment(models.TextChoices):
        CREDIT_CARD = 'Credit Card', 'Credit Card'
        CASH_ON_DELIVERY = 'Cash on Delivery', 'Cash on Delivery'
        PAYPAL = 'Paypal', 'Paypal'
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_item_id = models.ManyToManyField(OrderItem)
    payment = models.CharField(
        max_length=20,
        choices=Payment.choices,
        default=Payment.CREDIT_CARD
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PREPARE
    )
    total_amount = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)
