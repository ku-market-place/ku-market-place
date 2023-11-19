"""This module contains the Product class."""
from django.db import models


class Product(models.Model):
    """Class for product table."""

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
    image = models.CharField(max_length=300, blank=True)

    def description(self):
        """
        Return a formatted string containing all description attributes of the Product.
        """
        description = f"Gender: {self.gender}\n"
        description += f"Master Category: {self.masterCategory}\n"
        description += f"Sub Category: {self.subCategory}\n"
        description += f"Article Type: {self.articleType}\n"
        description += f"Base Colour: {self.baseColour}\n"
        description += f"Season: {self.season}\n"
        description += f"Year: {self.year}\n"
        description += f"Usage: {self.usage}\n"

        return description

    def __str__(self):
        """Return product name."""
        return self.productDisplayName
