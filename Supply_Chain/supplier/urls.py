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

    path('purchase_order/', views.purchase_order_supplier, name = 'purchase-order-supplier'),
    path('purchase_order/new', views.new_purchase_order_supplier, name = 'new-purchase-order-supplier'),
    path('purchase_order/edit/<pk>', views.edit_purchase_order_supplier, name = 'edit-purchase-order-supplier'),

    path('delivery_challan/', views.delivery_challan_supplier, name = 'delivery-challan-supplier'),
    path('delivery_challan/new', views.new_delivery_challan_supplier, name = 'new-delivery-challan-supplier'),
    path('delivery_challan/edit/<pk>', views.edit_delivery_challan_supplier, name = 'edit-delivery-challan-supplier'),

    path('mrn/', views.mrn_supplier, name = 'mrn-supplier'),
    path('mrn/edit/<pk>', views.edit_mrn_supplier, name = 'edit-mrn-supplier'),
]
