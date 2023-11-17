from django.db import models
from django.utils import timezone


class Product(models.Model):

    product_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', default=timezone.now)
