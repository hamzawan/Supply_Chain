from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import PurchaseHeader, PurchaseDetail, SaleHeader, SaleDetail, ChartOfAccount, PurchaseReturnHeader, PurchaseReturnDetail, SaleReturnHeader, SaleReturnDetail
from inventory.models import Add_products
from django.core import serializers
from django.db.models import Q
import json, datetime


def purchase(request):
    all_purchases = PurchaseHeader.objects.all()
    return render(request, 'transaction/purchase.html',{'all_purchases': all_purchases})


def new_purchase(request):
    all_item_code = Add_products.objects.all()
    all_accounts = ChartOfAccount.objects.all()
    for value in all_item_code:
        print(value.product_code)
    get_last_purchase_no = PurchaseHeader.objects.last()
    if get_last_purchase_no:
        get_last_purchase_no = get_last_purchase_no.purchase_no
        get_last_purchase_no = get_last_purchase_no[-3:]
        num = int(get_last_purchase_no)
        num = num + 1
        get_last_purchase_no = 'PUR/' + str(num)
    else:
        get_last_purchase_no = 'PUR/101'
    item_code = request.POST.get('item_code_purchase',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id',False)
        supplier = request.POST.get('supplier',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        withholding_tax = request.POST.get('withholding_tax',False)
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        date = datetime.date.today()

        purchase_header = PurchaseHeader(purchase_no = purchase_id, date = date, footer_description = footer_desc, payment_method = payment_method, cartage_amount = cartage_amount, additional_tax = additional_tax, withholding_tax = withholding_tax, account_id = account_id )

        items = json.loads(request.POST.get('items'))
        purchase_header.save()
        header_id = PurchaseHeader.objects.get(purchase_no = purchase_id)
        for value in items:
            purchase_detail = PurchaseDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], purchase_id = header_id)
            purchase_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/new_purchase.html',{'all_item_code':all_item_code,'get_last_purchase_no':get_last_purchase_no, 'all_accounts':all_accounts})

def purchase_return_summary(request):
    all_purchase_return = PurchaseReturnHeader.objects.all()
    return render(request, 'transaction/purchase_return_summary.html',{'all_purchase_return': all_purchase_return})


def new_purchase_return(request,pk):
    get_last_purchase_no = PurchaseReturnHeader.objects.last()
    if get_last_purchase_no:
        get_last_purchase_no = get_last_purchase_no.purchase_no
        get_last_purchase_no = get_last_purchase_no[-3:]
        num = int(get_last_purchase_no)
        num = num + 1
        get_last_purchase_no = 'PUR/RET/' + str(num)
    else:
        get_last_purchase_no = 'PUR/RET/101'
    purchase_header = PurchaseHeader.objects.filter(id = pk).first()
    purchase_detail = PurchaseDetail.objects.filter(purchase_id = pk).all()
    if request.method == 'POST':
        supplier = request.POST.get('supplier',False)
        print(supplier)
        payment_method = request.POST.get('payment_method',False)
        description = request.POST.get('description',False)
        date = datetime.date.today()
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        purchase_return_header = PurchaseReturnHeader(purchase_no = get_last_purchase_no, date = date, footer_description = description, payment_method = payment_method, cartage_amount = 0, additional_tax = 0, withholding_tax = 0, account_id = account_id )
        purchase_return_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = PurchaseReturnHeader.objects.get(purchase_no = get_last_purchase_no)
        for value in items:
            purchase_return_detail = PurchaseReturnDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], purchase_return_id = header_id)
            purchase_return_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/purchase_return.html',{'purchase_header':purchase_header, 'purchase_detail': purchase_detail,'pk':pk})


def sale(request):
    all_sales = SaleHeader.objects.all()
    return render(request, 'transaction/sale.html',{'all_sales': all_sales})


def new_sale(request):
    all_item_code = Add_products.objects.all()
    all_accounts = ChartOfAccount.objects.all()
    for value in all_item_code:
        print(value.product_code)
    get_last_sale_no = SaleHeader.objects.last()
    if get_last_sale_no:
        get_last_sale_no = get_last_sale_no.sale_no
        get_last_sale_no = get_last_sale_no[-3:]
        num = int(get_last_sale_no)
        num = num + 1
        get_last_sale_no = 'SAL/' + str(num)
    else:
        get_last_sale_no = 'SAL/101'
    item_code = request.POST.get('item_code_sale',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id',False)
        customer = request.POST.get('customer',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        withholding_tax = request.POST.get('withholding_tax',False)
        account_id = ChartOfAccount.objects.get(account_title = customer)
        date = datetime.date.today()

        sale_header = SaleHeader(sale_no = sale_id, date = date, footer_description = footer_desc, payment_method = payment_method, cartage_amount = cartage_amount, additional_tax = additional_tax, withholding_tax = withholding_tax, account_id = account_id )

        items = json.loads(request.POST.get('items'))
        sale_header.save()
        header_id = SaleHeader.objects.get(sale_no = sale_id)
        for value in items:
            sale_detail = SaleDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], sale_id = header_id)
            sale_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/new_sales.html',{'all_item_code':all_item_code,'get_last_sale_no':get_last_sale_no, 'all_accounts':all_accounts})

def sale_return_summary(request):
    all_sales_return = SaleReturnHeader.objects.all()
    return render(request, 'transaction/sale_return_summary.html',{'all_sales_return': all_sales_return})


def new_sale_return(request,pk):
    get_last_sale_no = SaleReturnHeader.objects.last()
    if get_last_sale_no:
        get_last_sale_no = get_last_sale_no.sale_no
        get_last_sale_no = get_last_sale_no[-3:]
        num = int(get_last_sale_no)
        num = num + 1
        get_last_sale_no = 'SAL/RET/' + str(num)
    else:
        get_last_sale_no = 'SAL/RET/101'
    sale_header = SaleHeader.objects.filter(id = pk).first()
    sale_detail = SaleDetail.objects.filter(sale_id = pk).all()
    if request.method == 'POST':
        customer = request.POST.get('customer',False)
        payment_method = request.POST.get('payment_method',False)
        description = request.POST.get('description',False)
        date = datetime.date.today()
        account_id = ChartOfAccount.objects.get(account_title = customer)
        sale_return_header = SaleReturnHeader(sale_no = get_last_sale_no, date = date, footer_description = description, payment_method = payment_method, cartage_amount = 0, additional_tax = 0, withholding_tax = 0, account_id = account_id )
        sale_return_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = SaleReturnHeader.objects.get(sale_no = get_last_sale_no)
        for value in items:
            sale_return_detail = SaleReturnDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"],unit = value["unit"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], sale_return_id = header_id)
            sale_return_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/sale_return.html',{'sale_header':sale_header, 'sale_detail': sale_detail,'pk':pk})



def chart_of_account(request):
    return render(request, 'transaction/chart_of_account.html')
