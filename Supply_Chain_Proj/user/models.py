from django.db import models
from django.contrib.auth.models import User


class UserRoles(models.Model):
    user_id = models.ForeignKey(User, models.SET_NULL,blank=True,null=True)
    form_id = models.IntegerField()
    form_name = models.CharField(max_length = 100)
    child_form = models.IntegerField()
    display = models.IntegerField()
    add = models.IntegerField()
    edit = models.IntegerField()
    delete = models.IntegerField()
    r_print = models.IntegerField()
