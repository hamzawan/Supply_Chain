from django.db import models
from transaction.models import ChartOfAccount
import datetime
from django.contrib.auth.models import User

class RfqSupplierHeader(models.Model):
    rfq_no = models.CharField(max_length = 100)
    date = models.DateField(default = datetime.date.today)
    attn = models.CharField(max_length = 100)
    follow_up = models.DateField(blank = True)
    show_notification = models.BooleanField(default = True)
    footer_remarks = models.TextField()
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True,)
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)


class RfqSupplierDetail(models.Model):
    item_code = models.CharField(max_length = 100)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length = 100)
    rfq_id = models.ForeignKey(RfqSupplierHeader, on_delete = models.CASCADE)


class QuotationHeaderSupplier(models.Model):
    quotation_no = models.CharField(max_length = 100)
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
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)


class QuotationDetailSupplier(models.Model):
    item_code = models.CharField(max_length = 100)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length = 100)
    unit_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    remarks = models.CharField(max_length = 100)
    quotation_id = models.ForeignKey(QuotationHeaderSupplier, on_delete = models.CASCADE)


class PoHeaderSupplier(models.Model):
    po_no = models.CharField(max_length = 100)
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
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)



class PoDetailSupplier(models.Model):
    item_code = models.CharField(max_length = 100)
    item_name = models.CharField(max_length = 100)
    item_description = models.TextField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length = 100)
    unit_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    remarks = models.CharField(max_length = 100)
    quotation_no = models.CharField(max_length = 100)
    footer_remarks = models.TextField()
    po_id = models.ForeignKey(PoHeaderSupplier, on_delete = models.CASCADE)


class DcHeaderSupplier(models.Model):
    dc_no = models.CharField(max_length = 100)
    date = models.DateField(default = datetime.date.today)
    footer_remarks = models.TextField()
    show_notification = models.BooleanField(default = True)
    follow_up = models.DateField(blank = True)
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True,)
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)


class DcDetailSupplier(models.Model):
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
    dc_id = models.ForeignKey(DcHeaderSupplier, on_delete = models.CASCADE)


class Company_info(models.Model):
    company_name = models.CharField(max_length = 100)
    company_address = models.TextField()
    company_logo = models.TextField()
    phone_no = models.CharField(max_length = 100)
    mobile_no = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    website = models.CharField(max_length = 100)
    ntn = models.CharField(max_length = 100)
    stn = models.CharField(max_length = 100)
    cnic = models.CharField(max_length = 100)
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)
