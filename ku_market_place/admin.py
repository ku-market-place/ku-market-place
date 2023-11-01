from django.contrib import admin
from ku_market_place.models import *

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Shipping)
admin.site.register(Customer)