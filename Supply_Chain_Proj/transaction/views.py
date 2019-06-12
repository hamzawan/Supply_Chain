from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import (PurchaseHeader, PurchaseDetail, SaleHeader, SaleDetail, ChartOfAccount,
                    PurchaseReturnHeader, PurchaseReturnDetail, SaleReturnHeader, SaleReturnDetail,
                    Transactions)
from supplier.models import Company_info
from inventory.models import Add_products
from django.core import serializers
from django.db.models import Q
import json, datetime
from supplier.utils import render_to_pdf
from django.template.loader import get_template
from django.db import connection


def purchase(request):
    all_purchases = PurchaseHeader.objects.all()
    return render(request, 'transaction/purchase.html',{'all_purchases': all_purchases})


def new_purchase(request):
    amount = 0
    item_amount = 0
    sales_tax = 0
    price = 0
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
            purchase_detail = PurchaseDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], unit = value["unit"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], purchase_id = header_id)
            purchase_detail.save()
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
        item_amount = item_amount + float(cartage_amount) + float(additional_tax)
        tax = ((item_amount * float(withholding_tax)) / 100)
        total_amount = tax + item_amount
        header_id = header_id.id
        total_amount = -abs(total_amount)
        print(total_amount)
        tran = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Invoice", amount = total_amount, date = date, remarks = "Amount Credit")
        tran.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/new_purchase.html',{'all_item_code':all_item_code,'get_last_purchase_no':get_last_purchase_no, 'all_accounts':all_accounts})

def edit_purchase(request,pk):
    all_item_code = Add_products.objects.all()
    purchase_header = PurchaseHeader.objects.filter(id = pk).first()
    purchase_detail = PurchaseDetail.objects.filter(purchase_id = pk).all()
    all_accounts = ChartOfAccount.objects.all()
    item_code = request.POST.get('item_code_purchase',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        purchase_detail.delete()

        purchase_id = request.POST.get('purchase_id',False)
        supplier = request.POST.get('supplier',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        withholding_tax = request.POST.get('withholding_tax',False)
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        date = datetime.date.today()
        purchase_header.payment_method = payment_method
        purchase_header.footer_description = footer_desc
        purchase_header.cartage_amount = cartage_amount
        purchase_header.additional_tax = additional_tax
        purchase_header.withholding_tax = withholding_tax
        purchase_header.account_id = account_id

        purchase_header.save()

        items = json.loads(request.POST.get('items'))
        purchase_header.save()
        header_id = PurchaseHeader.objects.get(purchase_no = purchase_id)
        for value in items:
            purchase_detail = PurchaseDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], unit = value["unit"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], purchase_id = header_id)
            purchase_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/edit_purchase.html',{'all_item_code':all_item_code,'all_accounts':all_accounts, 'purchase_header':purchase_header, 'purchase_detail':purchase_detail, 'pk':pk})



def purchase_return_summary(request):
    all_purchase_return = PurchaseReturnHeader.objects.all()
    return render(request, 'transaction/purchase_return_summary.html',{'all_purchase_return': all_purchase_return})


def new_purchase_return(request,pk):
    total_amount = 0
    item_amount = 0
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
        payment_method = request.POST.get('payment_method',False)
        description = request.POST.get('description',False)
        date = datetime.date.today()
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        purchase_return_header = PurchaseReturnHeader(purchase_no = get_last_purchase_no, date = date, footer_description = description, payment_method = payment_method, cartage_amount = 0, additional_tax = 0, withholding_tax = 0, account_id = account_id )
        purchase_return_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = PurchaseReturnHeader.objects.get(purchase_no = get_last_purchase_no)
        for value in items:
            purchase_return_detail = PurchaseReturnDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"],unit = value["unit"] ,cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], purchase_return_id = header_id)
            purchase_return_detail.save()
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            total_amount = item_amount + amount
        header_id = header_id.id
        tran = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Return", amount = total_amount, date = date, remarks = "Purchase return against "+purchase_header.purchase_no+" invoice")
        tran.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/purchase_return.html',{'purchase_header':purchase_header, 'purchase_detail': purchase_detail,'pk':pk})

def edit_purchase_return(request,pk):
    purchase_header = PurchaseReturnHeader.objects.filter(id = pk).first()
    purchase_detail = PurchaseReturnDetail.objects.filter(purchase_return_id = pk).all()
    all_accounts = ChartOfAccount.objects.all()
    if request.method == 'POST':
        purchase_detail.delete()
        purchase_id = request.POST.get('purchase_id',False)
        supplier = request.POST.get('supplier',False)
        payment_method = request.POST.get('payment_method',False)
        description = request.POST.get('footer_desc',False)
        date = datetime.date.today()

        account_id = ChartOfAccount.objects.get(account_title = supplier)
        purchase_header.payment_method = payment_method
        purchase_header.footer_description = description
        purchase_header.account_id = account_id

        purchase_header.save()
        items = json.loads(request.POST.get('items'))
        print(items)
        header_id = PurchaseReturnHeader.objects.get(purchase_no = purchase_id)
        for value in items:
            purchase_return_detail = PurchaseReturnDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"],unit = value["unit"] ,cost_price = value["price"], retail_price = 0.00, sales_tax = value["sales_tax"], purchase_return_id = header_id)
            purchase_return_detail.save()
            print(value["sales_tax"])
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/edit_purchase_return.html',{'purchase_header':purchase_header, 'purchase_detail': purchase_detail,'pk':pk,'all_accounts':all_accounts})


def sale(request):
    all_sales = SaleHeader.objects.all()
    return render(request, 'transaction/sale.html',{'all_sales': all_sales})


def new_sale(request):
    item_amount = 0
    total_amount = 0
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
            sale_detail = SaleDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"],unit = value["unit"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], sale_id = header_id)
            sale_detail.save()
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
        item_amount = item_amount + float(cartage_amount) + float(additional_tax)
        tax = ((item_amount * float(withholding_tax)) / 100)
        total_amount = tax + item_amount
        header_id = header_id.id
        tran = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Invoice", amount = total_amount, date = date, remarks = "Amount Debit")
        tran.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/new_sales.html',{'all_item_code':all_item_code,'get_last_sale_no':get_last_sale_no, 'all_accounts':all_accounts})


def edit_sale(request,pk):
    all_item_code = Add_products.objects.all()
    sale_header = SaleHeader.objects.filter(id = pk).first()
    sale_detail = SaleDetail.objects.filter(sale_id = pk).all()
    all_accounts = ChartOfAccount.objects.all()
    item_code = request.POST.get('item_code_sale',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        sale_detail.delete()

        sale_id = request.POST.get('sale_id',False)
        customer = request.POST.get('customer',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        withholding_tax = request.POST.get('withholding_tax',False)
        account_id = ChartOfAccount.objects.get(account_title = customer)
        date = datetime.date.today()
        sale_header.payment_method = payment_method
        sale_header.footer_description = footer_desc
        sale_header.cartage_amount = cartage_amount
        sale_header.additional_tax = additional_tax
        sale_header.withholding_tax = withholding_tax
        sale_header.account_id = account_id

        sale_header.save()

        items = json.loads(request.POST.get('items'))
        sale_header.save()
        print(sale_id)
        header_id = SaleHeader.objects.get(sale_no = sale_id)
        for value in items:
            sale_detail = SaleDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], unit = value["unit"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], sale_id = header_id)
            sale_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/edit_sale.html',{'all_item_code':all_item_code,'all_accounts':all_accounts, 'sale_header':sale_header, 'sale_detail':sale_detail, 'pk':pk})


def sale_return_summary(request):
    all_sales_return = SaleReturnHeader.objects.all()
    return render(request, 'transaction/sale_return_summary.html',{'all_sales_return': all_sales_return})


def new_sale_return(request,pk):
    item_amount = 0
    total_amount = 0
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
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            total_amount = item_amount + amount
        header_id = header_id.id
        total_amount = -abs(total_amount)
        tran = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Return", amount = total_amount, date = date, remarks = "Sale return against "+sale_header.sale_no+" invoice")
        tran.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/sale_return.html',{'sale_header':sale_header, 'sale_detail': sale_detail,'pk':pk})


def edit_sale_return(request,pk):
    sale_header = SaleReturnHeader.objects.filter(id = pk).first()
    sale_detail = SaleReturnDetail.objects.filter(sale_return_id = pk).all()
    all_accounts = ChartOfAccount.objects.all()
    if request.method == 'POST':
        sale_detail.delete()
        sale_id = request.POST.get('sale_id',False)
        customer = request.POST.get('customer',False)
        payment_method = request.POST.get('payment_method',False)
        description = request.POST.get('footer_desc',False)
        date = datetime.date.today()

        account_id = ChartOfAccount.objects.get(account_title = customer)
        sale_header.payment_method = payment_method
        sale_header.footer_description = description
        sale_header.account_id = account_id

        sale_header.save()
        items = json.loads(request.POST.get('items'))
        print(items)
        header_id = SaleReturnHeader.objects.get(sale_no = sale_id)
        for value in items:
            sale_return_detail = SaleReturnDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"],unit = value["unit"] ,cost_price = value["price"], retail_price = 0.00, sales_tax = value["sales_tax"], sale_return_id = header_id)
            sale_return_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/edit_sale_return.html',{'sale_header':sale_header, 'sale_detail': sale_detail,'pk':pk,'all_accounts':all_accounts})



def chart_of_account(request):
    if request.method == 'POST':
        account_title = request.POST.get('account_title')
        account_type = request.POST.get('account_type')
        opening_balance = request.POST.get('opening_balance')
        phone_no = request.POST.get('phone_no')
        email_address = request.POST.get('email_address')
        ntn = request.POST.get('ntn')
        address = request.POST.get('address')
        remarks = request.POST.get('remarks')
        op_type = request.POST.get('optradio')

        if opening_balance is "":
            opening_balance = 0
        if op_type == "credit":
            opening_balance = -abs(int(opening_balance))
        coa = ChartOfAccount(account_title = account_title, parent_id = account_type, opening_balance = opening_balance, phone_no = phone_no, email_address = email_address, ntn = ntn, Address = address, remarks = remarks)
        coa.save()
    customer_accounts = ChartOfAccount.objects.filter(parent_id = 1)
    supplier_accounts = ChartOfAccount.objects.filter(parent_id = 2)
    return render(request, 'transaction/chart_of_account.html',{'customer_accounts':customer_accounts, 'supplier_accounts':supplier_accounts})


def reports(request):
    all_accounts = ChartOfAccount.objects.all()
    return render(request,'transaction/reports.html',{'all_accounts':all_accounts})

def journal_voucher(request):
    all_accounts = ChartOfAccount.objects.all()
    return render(request, 'transaction/journal_voucher.html',{"all_accounts":all_accounts})





def account_ledger(request):
    if request.method == "POST":
        debit_amount = 0
        credit_amount = 0
        pk = request.POST.get('account_title')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        company_info = Company_info.objects.all()
        image = Company_info.objects.filter(company_name = "Hamza Enterprise").first()
        cursor = connection.cursor()
        cursor.execute('''Select tran_type,refrence_id,refrence_date,remarks,voucher_no,
                        Case When amount > -1 Then  amount Else 0 End As Debit,
                        Case When amount < -1 Then  amount Else 0 End As Credit
                        From transaction_transactions
                        Where transaction_transactions.date Between %s And %s and transaction_transactions.account_id_id = %s
                        Order By refrence_date Asc
                    ''',[from_date, to_date, pk])
        row = cursor.fetchall()
        for value in row:
            print(value)
        if row:
            for v in row:
                if v[5] >= 0:
                    debit_amount = debit_amount + v[5]
                if v[6] <= 0:
                    credit_amount = credit_amount + v[6]
        print(debit_amount)
        print(credit_amount)
        pdf = render_to_pdf('transaction/account_ledger_pdf.html', {'company_info':company_info,'image':image,'row':row, 'debit_amount':debit_amount, 'credit_amount': credit_amount})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "TrialBalance%s.pdf" %("000")
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('report')


def trial_balance(request):
    if request.method == "POST":
        debit_amount = 0;
        credit_amount = 0;
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        company_info = Company_info.objects.all()
        image = Company_info.objects.filter(company_name = "Hamza Enterprise").first()
        cursor = connection.cursor()
        cursor.execute('''Select id,account_title,ifnull(amount,0) + opening_balance As Amount
                        from transaction_chartofaccount
                        Left Join
                        (select account_id_id,sum(AMount) As Amount from transaction_transactions
                        Where transaction_transactions.date Between %s And %s
                        Group By account_id_id) As tbltran On transaction_chartofaccount.id = tbltran.account_id_id
                        ''',[from_date, to_date])
        row = cursor.fetchall()
        for v in row:
            if v[2] >= 0:
                debit_amount = debit_amount + v[2]
            else:
                credit_amount = credit_amount + v[2]
        pdf = render_to_pdf('transaction/trial_balance_pdf.html', {'company_info':company_info,'image':image,'row':row, 'debit_amount':debit_amount, 'credit_amount': credit_amount})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "TrialBalance%s.pdf" %("000")
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('report')
