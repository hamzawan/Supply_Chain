from django.urls import path, include
from . import views


urlpatterns = [
    path('purchase/', views.purchase, name = 'purchase'),
    path('purchase/new/', views.new_purchase, name = 'new-purchase'),
    path('purchase_return_summary/', views.purchase_return_summary, name = 'purchase-return-summary'),
    path('purchase/return/<pk>', views.new_purchase_return, name = 'new-purchase-return'),
    path('chart_of_account/new', views.chart_of_account, name = 'chart-of-account'),


    path('sale/', views.sale, name = 'sale'),
    path('sale/new/', views.new_sale, name = 'new-sale'),
    path('sale_return_summary/', views.sale_return_summary, name = 'sale-return-summary'),
    path('sale/return/<pk>', views.new_sale_return, name = 'new-sale-return'),

]
