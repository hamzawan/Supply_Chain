from django.db import models


class Add_products(models.Model):
    product_code = models.CharField(max_length = 100, unique = True)
    product_name = models.CharField(max_length = 100)
    product_desc = models.CharField(max_length = 100)
