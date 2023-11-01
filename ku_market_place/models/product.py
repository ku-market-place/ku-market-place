from django.db import models


class Product(models.Model):

    product_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)