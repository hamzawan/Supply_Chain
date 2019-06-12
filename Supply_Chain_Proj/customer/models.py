from django.db import models
from transaction.models import ChartOfAccount
import datetime

class RfqCustomerHeader(models.Model):
    rfq_no = models.CharField(max_length = 100, unique = True)
    date = models.DateField(default = datetime.date.today)
    attn = models.CharField(max_length = 100)
    follow_up = models.DateField(blank = True)
    show_notification = models.BooleanField(default = True)
    footer_remarks = models.TextField()
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True,)

class RfqCustomerDetail(models.Model):
    item_code = models.CharField(max_length = 100, unique = True)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length = 100)
    rfq_id = models.ForeignKey(RfqCustomerHeader, on_delete = models.CASCADE)


class QuotationHeaderCustomer(models.Model):
    quotation_no = models.CharField(max_length = 100, unique = True)
    date = models.DateField(default = datetime.date.today)
    attn = models.CharField(max_length = 100)
    prc_basis = models.CharField(max_length = 100)
    leadtime = models.CharField(max_length = 100)
    validity = models.CharField(max_length = 100)
    payment = models.CharField(max_length = 100)
    remarks = models.CharField(max_length = 100)
    currency = models.CharField(max_length = 100)
    exchange_rate = models.DecimalField(max_digits = 8, decimal_places = 2)
    follow_up = models.DateField(blank = True)
    show_notification = models.BooleanField(default = True)
    footer_remarks = models.TextField()
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True,)


class QuotationDetailCustomer(models.Model):
    item_code = models.CharField(max_length = 100, unique = True)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length = 100)
    unit_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    remarks = models.CharField(max_length = 100)
    quotation_id = models.ForeignKey(QuotationHeaderCustomer, on_delete = models.CASCADE)


class PoHeaderCustomer(models.Model):
    po_no = models.CharField(max_length = 100, unique = True)
    date = models.DateField(default = datetime.date.today)
    attn = models.CharField(max_length = 100)
    prc_basis = models.CharField(max_length = 100)
    yrref = models.CharField(max_length = 100)
    leadtime = models.CharField(max_length = 100)
    validity = models.CharField(max_length = 100)
    payment = models.CharField(max_length = 100)
    remarks = models.CharField(max_length = 100)
    currency = models.CharField(max_length = 100)
    exchange_rate = models.DecimalField(max_digits = 8, decimal_places = 2)
    follow_up = models.DateField(blank = True)
    show_notification = models.BooleanField(default = True)
    footer_remarks = models.TextField()
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True,)


class PoDetailCustomer(models.Model):
    item_code = models.CharField(max_length = 100, unique = True)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length = 100)
    unit_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    remarks = models.CharField(max_length = 100)
    quotation_no = models.CharField(max_length = 100)
    po_id = models.ForeignKey(PoHeaderCustomer, on_delete = models.CASCADE)


class DcHeaderCustomer(models.Model):
    dc_no = models.CharField(max_length = 100)
    date = models.DateField(default = datetime.date.today)
    footer_remarks = models.TextField()
    follow_up = models.DateField(blank = True)
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True,)

class DcDetailCustomer(models.Model):
    item_code = models.CharField(max_length = 100)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    quantity = models.IntegerField()
    accepted_quantity = models.IntegerField()
    returned_quantity = models.IntegerField()
    unit = models.CharField(max_length = 100)
    unit_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    remarks = models.CharField(max_length = 100)
    po_no = models.CharField(max_length = 100)
    dc_id = models.ForeignKey(DcHeaderCustomer, on_delete = models.CASCADE)
