from django.db import models
import datetime

class PurchaseHeader(models.Model):
    date = models.DateField(default = datetime.date.today)
    footer_description = models.TextField()
    payment_method = models.CharField(max_length = 100)
    cartage_amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    additional_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    withholding_tax = models.DecimalField(max_digits = 8, decimal_places = 2)

class PurchaseDetail(models.Model):
    item_code = models.CharField(max_length = 100)
    item_name = models.CharField(max_length = 100)
    item_description = models.CharField(max_length = 100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits = 8, decimal_places = 2)
    retail_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    sales_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    transaction_id = models.ForeignKey(PurchaseHeader, on_delete = models.CASCADE)
