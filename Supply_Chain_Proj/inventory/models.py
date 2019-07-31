from django.db import models
from django.contrib.auth.models import User


class Add_products(models.Model):
    product_code = models.CharField(max_length = 100, unique = True)
    product_name = models.CharField(max_length = 100)
    product_desc = models.TextField()
    unit = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100)
    size = models.CharField(max_length = 100)
    opening_stock = models.DecimalField(max_digits = 8, decimal_places = 2)
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)
