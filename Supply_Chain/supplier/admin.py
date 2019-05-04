from django.contrib import admin
from .models import (RfqSupplierHeader, RfqSupplierDetail,
                    QuotationHeaderSupplier, QuotationDetailSupplier,
                    PoHeaderSupplier, PoDetailSupplier,
                    DcHeaderSupplier, DcDetailSupplier)

admin.site.register(RfqSupplierHeader)
admin.site.register(RfqSupplierDetail)
admin.site.register(QuotationHeaderSupplier)
admin.site.register(QuotationDetailSupplier)
admin.site.register(PoHeaderSupplier)
admin.site.register(PoDetailSupplier)
admin.site.register(DcHeaderSupplier)
admin.site.register(DcDetailSupplier)
