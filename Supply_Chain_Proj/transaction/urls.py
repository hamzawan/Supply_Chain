from django.urls import path, include
from . import views


urlpatterns = [

    path('chart_of_account/new', views.chart_of_account, name = 'chart-of-account'),
    path('reports/', views.reports, name = 'report'),

    path('purchase/', views.purchase, name = 'purchase'),
    path('purchase/new/', views.new_purchase, name = 'new-purchase'),
    path('purchase/edit/<pk>', views.edit_purchase, name = 'edit-purchase'),

    path('purchase_return_summary/', views.purchase_return_summary, name = 'purchase-return-summary'),
    path('purchase/return/<pk>', views.new_purchase_return, name = 'new-purchase-return'),
    path('purchase/return/edit/<pk>/', views.edit_purchase_return, name = 'edit-purchase-return'),



    path('sale/', views.sale, name = 'sale'),
    path('sale/new/', views.new_sale, name = 'new-sale'),
    path('sale/edit/<pk>', views.edit_sale, name = 'edit-sale'),


    path('sale_return_summary/', views.sale_return_summary, name = 'sale-return-summary'),
    path('sale/return/<pk>', views.new_sale_return, name = 'new-sale-return'),
    path('sale/return/edit/<pk>', views.edit_sale_return, name = 'edit-sale-return'),

    path('journal_voucher/new', views.journal_voucher, name = 'journal-voucher'),
    path('trial_balance/pdf', views.trial_balance, name = 'trial-balance'),
    path('account_ledger/pdf/', views.account_ledger, name = 'account-ledger'),
    path('trial_balance/pdf/', views.trial_balance, name = 'trial-balance'),


]
