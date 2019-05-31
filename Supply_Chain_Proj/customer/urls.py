from django.urls import path, include
from . import views


urlpatterns = [
    path('rfq/', views.rfq_customer, name = 'rfq-customer'),
    path('rfq/new/', views.new_rfq_customer, name = 'new-rfq-customer'),
    path('rfq/edit/<pk>', views.edit_rfq_customer, name = 'edit-rfq-customer'),

    path('quotation/', views.quotation_customer, name = 'quotation-customer'),
    path('quotation/new', views.new_quotation_customer, name = 'new-quotation-customer'),
    path('quotation/edit/<pk>', views.edit_quotation_customer, name = 'edit-quotation-customer'),
    path('print_quotation_customer/<pk>', views.print_quotation_customer, name = 'print-quotation-customer'),

    path('purchase_order/', views.purchase_order_customer, name = 'purchase-order-customer'),
    path('purchase_order/new', views.new_purchase_order_customer, name = 'new-purchase-order-customer'),
    path('purchase_order/edit/<pk>', views.edit_purchase_order_customer, name = 'edit-purchase-order-customer'),
    path('print_po_customer/<pk>', views.print_po_customer, name = 'print-po-customer'),

    path('delivery_challan/', views.delivery_challan_customer, name = 'delivery-challan-customer'),
    path('delivery_challan/new', views.new_delivery_challan_customer, name = 'new-delivery-challan-customer'),
    path('delivery_challan/edit/<pk>', views.edit_delivery_challan_customer, name = 'edit-delivery-challan-customer'),
    path('print_dc_customer/<pk>', views.print_dc_customer, name = 'print-dc-customer'),

    path('mrn/', views.mrn_customer, name = 'mrn-customer'),
    path('mrn/edit/<pk>', views.edit_mrn_customer, name = 'edit-mrn-customer'),
]
