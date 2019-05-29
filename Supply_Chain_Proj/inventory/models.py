from django.db import models


class Add_products(models.Model):
    product_code = models.CharField(max_length = 100, unique = True)
    product_name = models.CharField(max_length = 100)
    product_desc = models.CharField(max_length = 100)
    unit = models.CharField(max_length = 100)
    opening_stock = models.DecimalField(max_digits = 8, decimal_places = 2)
