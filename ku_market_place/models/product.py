from django.db import models


class Product(models.Model):
    gender = models.CharField(max_length=10, default='Unisex')
    masterCategory = models.CharField(max_length=50, blank=True)
    subCategory = models.CharField(max_length=50, blank=True)
    articleType = models.CharField(max_length=50, blank=True)
    baseColour = models.CharField(max_length=50, blank=True)
    season = models.CharField(max_length=20, blank=True)
    year = models.IntegerField(default=2023, blank=True)
    usage = models.CharField(max_length=20, blank=True)
    productDisplayName = models.CharField(max_length=255, blank=True)
    productPrice = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=100)

    def __str__(self):
        return self.productDisplayName
