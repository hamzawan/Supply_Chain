from django.contrib import admin
from .models import (PurchaseHeader, PurchaseDetail, SaleHeader, SaleDetail,
                    PurchaseReturnHeader,PurchaseReturnDetail,SaleReturnHeader, SaleReturnDetail ,ChartOfAccount, Transactions,
                    VoucherHeader, VoucherDetail)

admin.site.register(PurchaseHeader)
admin.site.register(PurchaseDetail)
admin.site.register(SaleHeader)
admin.site.register(SaleDetail)
admin.site.register(PurchaseReturnHeader)
admin.site.register(PurchaseReturnDetail)
admin.site.register(SaleReturnHeader)
admin.site.register(SaleReturnDetail)
admin.site.register(ChartOfAccount)
admin.site.register(Transactions)
admin.site.register(VoucherHeader)
admin.site.register(VoucherDetail)
