from django.db import models
import datetime

class PurchaseHeader(models.Model):
    date = models.DateField(default = datetime.date.today)
    footer_description = models.TextField()
    payment_method = models.CharField(max_length = 100)
    cartage_amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    additional_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    withholding_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    account_id = models.IntegerField()

class PurchaseDetail(models.Model):
    item_code = models.CharField(max_length = 100)
    item_name = models.CharField(max_length = 100)
    item_description = models.CharField(max_length = 100)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    retail_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    sales_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    purchase_id = models.ForeignKey(PurchaseHeader, on_delete = models.CASCADE)


class ChartOfAccount(models.Model):
    account_title = models.CharField(max_length = 100, unique = True)
    account_type = models.CharField(max_length = 100)
    opening_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    phone_no = models.CharField(max_length = 100)
    email_address = models.CharField(max_length = 100)
    ntn = models.CharField(max_length = 100)
    Address = models.CharField(max_length = 200)
    remarks = models.CharField(max_length = 100)
