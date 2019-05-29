from django.contrib import admin
from .models import (PurchaseHeader, PurchaseDetail, SaleHeader, SaleDetail,
                    PurchaseReturnHeader,PurchaseReturnDetail, ChartOfAccount)

admin.site.register(PurchaseHeader)
admin.site.register(PurchaseDetail)
admin.site.register(SaleHeader)
admin.site.register(SaleDetail)
admin.site.register(PurchaseReturnHeader)
admin.site.register(PurchaseReturnDetail)
admin.site.register(ChartOfAccount)
