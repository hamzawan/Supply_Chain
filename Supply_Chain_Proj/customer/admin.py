from django.contrib import admin
from .models import (RfqCustomerHeader, RfqCustomerDetail,
                    QuotationHeaderCustomer, QuotationDetailCustomer,
                    PoHeaderCustomer, PoDetailCustomer,
                    DcHeaderCustomer, DcDetailCustomer)


admin.site.register(RfqCustomerHeader)
admin.site.register(RfqCustomerDetail)
admin.site.register(QuotationHeaderCustomer)
admin.site.register(QuotationDetailCustomer)
admin.site.register(PoHeaderCustomer)
admin.site.register(PoDetailCustomer)
admin.site.register(DcHeaderCustomer)
admin.site.register(DcDetailCustomer)
