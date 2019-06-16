from django.urls import path, include
from . import views


urlpatterns = [

    path('', views.home, name = 'home'),
    path('rfq/', views.rfq_supplier, name = 'rfq-supplier'),
    path('rfq/new/', views.new_rfq_supplier, name = 'new-rfq-supplier'),
    path('rfq/edit/<pk>', views.edit_rfq_supplier, name = 'edit-rfq-supplier'),

    path('quotation/', views.quotation_supplier, name = 'quotation-supplier'),
    path('quotation/new', views.new_quotation_supplier, name = 'new-quotation-supplier'),
    path('quotation/edit/<pk>', views.edit_quotation_supplier, name = 'edit-quotation-supplier'),
    path('print_quotation_supplier/<pk>',views.print_quotation_supplier, name = 'print-quotation-supplier'),

    path('purchase_order/', views.purchase_order_supplier, name = 'purchase-order-supplier'),
    path('purchase_order/new', views.new_purchase_order_supplier, name = 'new-purchase-order-supplier'),
    path('purchase_order/edit/<pk>', views.edit_purchase_order_supplier, name = 'edit-purchase-order-supplier'),
    path('print_po_supplier/<pk>',views.print_po_supplier, name = 'print-po-supplier'),

    path('delivery_challan/', views.delivery_challan_supplier, name = 'delivery-challan-supplier'),
    path('delivery_challan/new', views.new_delivery_challan_supplier, name = 'new-delivery-challan-supplier'),
    path('delivery_challan/edit/<pk>', views.edit_delivery_challan_supplier, name = 'edit-delivery-challan-supplier'),
    path('print_dc_supplier/<pk>',views.print_dc_supplier, name = 'print-dc-supplier'),

    path('mrn/', views.mrn_supplier, name = 'mrn-supplier'),
    path('mrn/edit/<pk>', views.edit_mrn_supplier, name = 'edit-mrn-supplier'),

    path('show_notification/', views.show_notification, name = 'show-notification'),
    path('update_notification_customer/', views.update_notification_customer, name = 'update-notification-customer'),

    path('show_notification_supplier/', views.show_notification_supplier, name = 'show-notification-supplier'),
    path('update_notification_supplier/', views.update_notification_supplier, name = 'update-notification-supplier'),
]
