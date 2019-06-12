from django.db import models
import datetime


class ChartOfAccount(models.Model):
    account_title = models.CharField(max_length = 100, unique = True)
    parent_id = models.IntegerField()
    opening_balance = models.DecimalField(max_digits = 8, decimal_places = 2)
    phone_no = models.CharField(max_length = 100)
    email_address = models.CharField(max_length = 100)
    ntn = models.CharField(max_length = 100)
    Address = models.CharField(max_length = 200)
    remarks = models.CharField(max_length = 100)


class PurchaseHeader(models.Model):
    purchase_no = models.CharField(max_length = 100, unique = True)
    date = models.DateField(default = datetime.date.today)
    footer_description = models.TextField()
    payment_method = models.CharField(max_length = 100)
    cartage_amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    additional_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    withholding_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True,)

class PurchaseDetail(models.Model):
    item_code = models.CharField(max_length = 100)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    unit = models.CharField(max_length = 100)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    retail_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    sales_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    purchase_id = models.ForeignKey(PurchaseHeader, on_delete = models.CASCADE)


class PurchaseReturnHeader(models.Model):
    purchase_no = models.CharField(max_length = 100, unique = True)
    date = models.DateField(default = datetime.date.today)
    footer_description = models.TextField()
    payment_method = models.CharField(max_length = 100)
    cartage_amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    additional_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    withholding_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True,)

class PurchaseReturnDetail(models.Model):
    item_code = models.CharField(max_length = 100)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    unit = models.CharField(max_length = 100)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    retail_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    sales_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    purchase_return_id = models.ForeignKey(PurchaseReturnHeader, on_delete = models.CASCADE)


class SaleHeader(models.Model):
    sale_no = models.CharField(max_length = 100, unique = True)
    date = models.DateField(default = datetime.date.today)
    footer_description = models.TextField()
    payment_method = models.CharField(max_length = 100)
    cartage_amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    additional_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    withholding_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True,)


class SaleDetail(models.Model):
    item_code = models.CharField(max_length = 100)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    unit = models.CharField(max_length = 100)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    retail_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    sales_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    sale_id = models.ForeignKey(SaleHeader, on_delete = models.CASCADE)


class SaleReturnHeader(models.Model):
    sale_no = models.CharField(max_length = 100, unique = True)
    date = models.DateField(default = datetime.date.today)
    footer_description = models.TextField()
    payment_method = models.CharField(max_length = 100)
    cartage_amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    additional_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    withholding_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True)

class SaleReturnDetail(models.Model):
    item_code = models.CharField(max_length = 100)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    unit = models.CharField(max_length = 100)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    retail_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    sales_tax = models.DecimalField(max_digits = 8, decimal_places = 2)
    sale_return_id = models.ForeignKey(SaleReturnHeader, on_delete = models.CASCADE)


class Transactions(models.Model):
    refrence_id = models.IntegerField()
    refrence_date = models.DateField(blank = True)
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True)
    tran_type = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    date = models.DateField(default = datetime.date.today)
    voucher_no = models.CharField(max_length = 100)
    remarks = models.CharField(max_length = 100)
