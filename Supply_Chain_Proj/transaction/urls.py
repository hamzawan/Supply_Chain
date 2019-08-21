from django.urls import path, include
from . import views


urlpatterns = [

    path('chart_of_account/new', views.chart_of_account, name = 'chart-of-account'),
    path('chart_of_account/edit', views.edit_chart_of_account, name = 'edit-chart-of-account'),
    path('chart_of_account/delete/<pk>', views.delete_chart_of_account, name = 'delete-chart-of-account'),
    path('reports/', views.reports, name = 'report'),

    path('purchase/', views.purchase, name = 'purchase'),
    path('purchase/new/', views.new_purchase, name = 'new-purchase'),
    path('purchase/edit/<pk>', views.edit_purchase, name = 'edit-purchase'),
    path('purchase/delete/<pk>', views.delete_purchase, name = 'delete-purchase'),

    path('purchase_return_summary/', views.purchase_return_summary, name = 'purchase-return-summary'),
    path('purchase/return/<pk>', views.new_purchase_return, name = 'new-purchase-return'),
    path('purchase/return/edit/<pk>/', views.edit_purchase_return, name = 'edit-purchase-return'),



    path('sale/', views.sale, name = 'sale'),
    path('sale/new/', views.new_sale, name = 'new-sale'),
    path('sale/edit/<pk>', views.edit_sale, name = 'edit-sale'),
    path('sale/delete/<pk>', views.delete_sale, name = 'delete-sale'),
    path('dc/sale/new/<pk>', views.direct_sale, name = 'direct-sale'),


    path('sale/new/ngst', views.new_sale_non_gst, name = 'new-sale-ngst'),
    path('sale/edit/ngst/<pk>', views.edit_sale_non_gst, name = 'edit-sale-ngst'),
    path('dc/sale/new/ngst/<pk>', views.direct_sale_non_gst, name = 'direct-sale-ngst'),


    path('purchase/new/ngst', views.new_purchase_non_gst, name = 'new-purchase-ngst'),
    path('purchase/edit/ngst/<pk>', views.edit_purchase_non_gst, name = 'edit-purchase-ngst'),


    path('sale_return_summary/', views.sale_return_summary, name = 'sale-return-summary'),
    path('sale/return/<pk>', views.new_sale_return, name = 'new-sale-return'),
    path('sale/return/edit/<pk>', views.edit_sale_return, name = 'edit-sale-return'),


    path('journal_voucher_summary/', views.journal_voucher_summary, name = 'journal-voucher-summary'),
    path('journal_voucher/new', views.journal_voucher, name = 'new-journal-voucher'),
    path('journal_voucher/edit/<pk>', views.edit_journal_voucher, name = 'edit-journal-voucher'),
    path('journal_voucher/delete/<pk>', views.delete_journal_voucher, name='delete-journal-voucher'),
    path('jv_pdf/<pk>', views.jv_pdf, name='jv-pdf'),


    path('cash_receiving_voucher', views.cash_receiving_voucher, name='cash-receiving-voucher'),
    path('cash_receiving_voucher/new/', views.new_cash_receiving_voucher, name='new-cash-receiving-voucher'),
    path('cash_receiving_voucher/view/<pk>', views.view_cash_receiving, name='view-cash-receiving'),
    path('cash_receiving_voucher/delete/<pk>', views.delete_cash_receiving, name='delete-cash-receiving'),
    path('crv_pdf/<pk>', views.crv_pdf, name='crv'),

    path('bank_receiving_voucher', views.bank_receiving_voucher, name='bank-receiving-voucher'),
    path('bank_receiving_voucher/new/', views.new_bank_receiving_voucher, name='new-bank-receiving-voucher'),
    path('bank_receiving_voucher/view/<pk>', views.view_bank_receiving, name='view-bank-receiving'),
    path('bank_receiving_voucher/delete/<pk>', views.delete_bank_receiving, name='delete-bank-receiving'),
    path('brv_pdf/<pk>', views.brv_pdf, name='brv'),

    path('bank_payment_voucher', views.bank_payment_voucher, name='bank-payment-voucher'),
    path('bank_payment_voucher/new/', views.new_bank_payment_voucher, name='new-bank-payment-voucher'),
    path('bank_payment_voucher/view/<pk>', views.view_bank_payment, name='view-bank-payment'),
    path('bank_payment_voucher/delete/<pk>', views.delete_bank_payment, name='delete-bank-payment'),
    path('bpv_pdf/<pk>', views.bpv_pdf, name='bpv'),

    path('cash_payment_voucher', views.cash_payment_voucher, name='cash-payment-voucher'),
    path('cash_payment_voucher/new/', views.new_cash_payment_voucher, name='new-cash-payment-voucher'),
    path('cash_payment_voucher/view/<pk>', views.view_cash_payment, name='view-cash-payment'),
    path('cash_payment_voucher/delete/<pk>', views.delete_cash_payment, name='delete-cash-payment'),
    path('cpv_pdf/<pk>', views.cpv_pdf, name='cpv'),

    path('trial_balance/pdf', views.trial_balance, name = 'trial-balance'),
    path('account_ledger/pdf/', views.account_ledger, name = 'account-ledger'),
    path('trial_balance/pdf/', views.trial_balance, name = 'trial-balance'),
    path('sale_detail/pdf/', views.sale_detail, name = 'sale-detail'),
    path('sale_detail_item_wise/pdf/', views.sale_detail_item_wise, name = 'sale-detail-item-wise'),
    path('sale_summary_item_wise/pdf/', views.sale_summary_item_wise, name = 'sale-summary-item-wise'),

    path('sales_tax_invoice/pdf/<pk>', views.sales_tax_invoice, name = 'sales-tax-invoice'),
    path('commercial_invoice/pdf/<pk>', views.commercial_invoice, name = 'commercial-invoice'),
    path('commercial_invoice/pdf/ngst/<pk>', views.commercial_invoice_non_gst, name = 'commercial-invoice-ngst'),


    path('companies/', views.multi_companies, name = 'multi-companies'),
    path('companies/new', views.new_multi_companies, name = 'new-multi-companies'),
    path('companies/edit/<pk>', views.edit_multi_companies, name = 'edit-multi-companies'),
    path('companies/delete/<pk>', views.delete_multi_companies, name = 'delete-multi-companies'),
]
