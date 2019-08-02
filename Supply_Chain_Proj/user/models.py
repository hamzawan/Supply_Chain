from django.db import models
from django.contrib.auth.models import User


class UserRoles(models.Model):
    user_id = models.ForeignKey(User, models.SET_NULL,blank=True,null=True)
    form_id = models.IntegerField()
    child_form = models.IntegerField()
    display = models.IntegerField()
    add = models.IntegerField()
    edit = models.IntegerField()
    delete = models.IntegerField()
    r_print = models.IntegerField()
    form_name = models.CharField(max_length = 100)
    r_return = models.IntegerField(default='0')


class FiscalYear(models.Model):
    fiscal_year = models.CharField(max_length = 100)
    database_name = models.CharField(max_length = 100)
    is_current_year = models.IntegerField()

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
