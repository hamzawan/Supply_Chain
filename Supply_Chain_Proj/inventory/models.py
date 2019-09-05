from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_code = models.IntegerField()
    main = models.CharField(max_length = 100)

class SubCategory(models.Model):
    sub_category_code = models.IntegerField()
    sub = models.CharField(max_length = 100)
    main_category_id = models.ForeignKey(Category, models.SET_NULL, blank = True, null = True)


class Add_products(models.Model):
    product_code = models.CharField(max_length = 100, unique = True)
    product_name = models.CharField(max_length = 100)
    product_desc = models.TextField()
    unit = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100)
    size = models.CharField(max_length = 100)
    opening_stock = models.DecimalField(max_digits = 8, decimal_places = 2)
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)
    main_category = models.CharField(max_length = 100)
    sub_category = models.CharField(max_length = 100)
    main_category_id = models.ForeignKey(Category, models.SET_NULL, blank = True, null = True)
    sub_category_id = models.ForeignKey(SubCategory, models.SET_NULL, blank = True, null = True)
