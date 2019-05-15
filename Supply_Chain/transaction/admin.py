from django.contrib import admin
from .models import (PurchaseHeader, PurchaseDetail)

admin.site.register(PurchaseHeader)
admin.site.register(PurchaseDetail)
