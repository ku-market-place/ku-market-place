"""Module contains the Customer model."""
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """Class for customer table."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    balance = models.IntegerField(default=10000)

    def __str__(self):
        return str(self.id) + " " + self.user.username