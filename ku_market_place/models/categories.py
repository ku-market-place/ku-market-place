from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    category_description = models.CharField(max_length=200)
    category_image = models.CharField(max_length=200)
    category_parent_id = models.IntegerField(default=0)
    category_status = models.IntegerField(default=0)
    category_date_added = models.DateTimeField('date added', null=True, blank=True)
    category_date_modified = models.DateTimeField('date modified', null=True, blank=True)
