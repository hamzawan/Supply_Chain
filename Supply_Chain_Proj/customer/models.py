from django.db import models
from transaction.models import ChartOfAccount
import datetime
from django.contrib.auth.models import User
from user.models import Company_info
from inventory.models import Add_products

class CompanyUser(models.Model):
    user_id = models.IntegerField()
    company_id = models.ForeignKey(Company_info, models.SET_NULL, blank = True, null = True)


class RfqCustomerHeader(models.Model):
    rfq_no = models.CharField(max_length = 100, unique = True)
    date = models.DateField(default = datetime.date.today)
    attn = models.CharField(max_length = 100)
    follow_up = models.DateField(blank = True)
    show_notification = models.BooleanField(default = True)
    footer_remarks = models.TextField()
    company_id = models.ForeignKey(Company_info, models.SET_NULL, blank = True, null = True)
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL, blank=True, null=True)
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)

class RfqCustomerDetail(models.Model):
    item_id = models.ForeignKey(Add_products, models.SET_NULL, blank = True, null = True)
    quantity = models.DecimalField(max_digits = 8, decimal_places = 2)
    rfq_id = models.ForeignKey(RfqCustomerHeader, on_delete = models.CASCADE)


class QuotationHeaderCustomer(models.Model):
    quotation_no = models.CharField(max_length = 100, unique = True)
    date = models.DateField(default = datetime.date.today)
    attn = models.CharField(max_length = 100)
    prc_basis = models.CharField(max_length = 100)
    leadtime = models.CharField(max_length = 100)
    validity = models.CharField(max_length = 100)
    payment = models.CharField(max_length = 100)
    yrref = models.CharField(max_length = 100)
    remarks = models.CharField(max_length = 100)
    currency = models.CharField(max_length = 100)
    exchange_rate = models.DecimalField(max_digits = 8, decimal_places = 2)
    follow_up = models.DateField(blank = True)
    show_notification = models.BooleanField(default = True)
    footer_remarks = models.TextField()
    company_id = models.ForeignKey(Company_info, models.SET_NULL, blank = True, null = True)
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True,)
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)

class QuotationDetailCustomer(models.Model):
    item_id = models.ForeignKey(Add_products, models.SET_NULL, blank = True, null = True)
    quantity = models.DecimalField(max_digits = 8, decimal_places = 2)
    unit_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    remarks = models.CharField(max_length = 100)
    quotation_id = models.ForeignKey(QuotationHeaderCustomer, on_delete = models.CASCADE)


class PoHeaderCustomer(models.Model):
    po_no = models.CharField(max_length = 100, unique = True)
    date = models.DateField(default = datetime.date.today)
    attn = models.CharField(max_length = 100)
    prc_basis = models.CharField(max_length = 100)
    po_client = models.CharField(max_length = 100)
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
    company_id = models.ForeignKey(Company_info, models.SET_NULL, blank = True, null = True)
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)

class PoDetailCustomer(models.Model):
    item_id = models.ForeignKey(Add_products, models.SET_NULL, blank = True, null = True)
    quantity = models.DecimalField(max_digits = 8, decimal_places = 2)
    unit_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    remarks = models.CharField(max_length = 100)
    quotation_no = models.CharField(max_length = 100)
    po_id = models.ForeignKey(PoHeaderCustomer, on_delete = models.CASCADE)


class DcHeaderCustomer(models.Model):
    dc_no = models.CharField(max_length = 100)
    date = models.DateField(default = datetime.date.today)
    footer_remarks = models.TextField()
    show_notification = models.BooleanField(default = True)
    follow_up = models.DateField(blank = True)
    cartage_amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    comments = models.CharField(max_length = 100)
    account_id = models.ForeignKey(ChartOfAccount, models.SET_NULL,blank=True,null=True)
    user_id = models.ForeignKey(User,models.SET_NULL, blank = True, null = True)
    company_id = models.ForeignKey(Company_info, models.SET_NULL, blank = True, null = True)


class DcDetailCustomer(models.Model):
    item_id = models.ForeignKey(Add_products, models.SET_NULL, blank = True, null = True)
    quantity = models.IntegerField()
    accepted_quantity = models.IntegerField()
    returned_quantity = models.IntegerField()
    po_no = models.CharField(max_length = 100)
    dc_id = models.ForeignKey(DcHeaderCustomer, on_delete = models.CASCADE)
