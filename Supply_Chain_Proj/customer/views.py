from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import (RfqCustomerHeader, RfqCustomerDetail,
                    QuotationHeaderCustomer, QuotationDetailCustomer,
                    PoHeaderCustomer, PoDetailCustomer,
                    DcHeaderCustomer, DcDetailCustomer)
from supplier.models import Company_info
from inventory.models import Add_products
from transaction.models import ChartOfAccount
from django.core import serializers
from django.forms.models import model_to_dict
import json
import datetime
from supplier.utils import render_to_pdf
from django.template.loader import get_template


def rfq_customer(request):
    all_rfq = RfqCustomerHeader.objects.all()
    return render(request, 'customer/rfq_customer.html',{'all_rfq':all_rfq})


def new_rfq_customer(request):
    get_last_rfq_no = RfqCustomerHeader.objects.last()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    if get_last_rfq_no:
        get_last_rfq_no = get_last_rfq_no.rfq_no
        get_last_rfq_no = get_last_rfq_no[-3:]
        num = int(get_last_rfq_no)
        num = num + 1
        get_last_rfq_no = 'RFQ/CU/' + str(num)
    else:
        get_last_rfq_no = 'RFQ/CU/101'
    item_code = request.POST.get('item_code',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        for value in data:
            print(value.product_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        customer = request.POST.get('customer',False)
        print(customer)
        attn = request.POST.get('attn',False)
        follow_up = request.POST.get('follow_up',False)
        footer_remarks = request.POST.get('footer_remarks',False)
        items = json.loads(request.POST.get('items'))
        account_id = ChartOfAccount.objects.get(account_title = customer)
        date = datetime.date.today()
        rfq_header = RfqCustomerHeader(rfq_no = get_last_rfq_no, date = date , attn = attn, follow_up = follow_up, footer_remarks = footer_remarks ,account_id = account_id)
        rfq_header.save()
        header_id = RfqCustomerHeader.objects.get(rfq_no=get_last_rfq_no)
        for value in items:
            rfq_detail = RfqCustomerDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], rfq_id = header_id)
            rfq_detail.save()
        return JsonResponse({"result": "success"})
    return render(request,'customer/new_rfq_customer.html',{'get_last_rfq_no':get_last_rfq_no,'all_item_code':all_item_code, 'all_accounts':all_accounts})


def edit_rfq_customer(request,pk):
    rfq_header = RfqCustomerHeader.objects.filter(id = pk).first()
    rfq_detail = RfqCustomerDetail.objects.filter(rfq_id = pk).all()
    all_accounts = ChartOfAccount.objects.all()
    all_item_code = list(Add_products.objects.values('product_code'))
    try:
        item_code = request.POST.get('item_code',False)
        if item_code:
            data = Add_products.objects.filter(product_code = item_code)
            item_code_exist = RfqCustomerDetail.objects.filter(item_code = item_code, rfq_id = pk).first()
            if item_code_exist:
                return HttpResponse(json.dumps({'message':"Item Already Exist"}))
            row = serializers.serialize('json',data)
            return HttpResponse(json.dumps({'row':row}))
        if request.method == 'POST':
            rfq_detail.delete()
            edit_rfq_customer = request.POST.get('customer',False)
            edit_rfq_attn = request.POST.get('edit_rfq_attn',False)
            edit_rfq_follow_up = request.POST.get('edit_rfq_follow_up',False)
            footer_remarks = request.POST.get('footer_remarks')
            account_id = ChartOfAccount.objects.get(account_title = edit_rfq_customer)

            rfq_header.account_id = account_id
            rfq_header.attn = edit_rfq_attn
            rfq_header.follow_up = edit_rfq_follow_up
            rfq_header.footer_remarks = footer_remarks
            rfq_header.save();
            header_id = RfqCustomerHeader.objects.get(id = pk)
            items = json.loads(request.POST.get('items'))
            for value in items:
                rfq_detail_update = RfqCustomerDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], unit = value["unit"], rfq_id = header_id)
                rfq_detail_update.save()
            return JsonResponse({"result":"success"})
    except IntegrityError:
        print("Data Already Exist")
    return render(request,'customer/edit_rfq_customer.html',{'rfq_header':rfq_header,'pk':pk,'rfq_detail':rfq_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts})


def quotation_customer(request):
    all_quotation = QuotationHeaderCustomer.objects.all()
    return render(request, 'customer/quotation_customer.html',{'all_quotation':all_quotation})


def new_quotation_customer(request):
    all_item_code = list(Add_products.objects.values('product_code'))
    get_last_quotation_no = QuotationHeaderCustomer.objects.last()
    all_accounts = ChartOfAccount.objects.all()
    if get_last_quotation_no:
        get_last_quotation_no = get_last_quotation_no.quotation_no
        get_last_quotation_no = get_last_quotation_no[-3:]
        num = int(get_last_quotation_no)
        num = num + 1
        get_last_quotation_no = 'QU/CU/' + str(num)
    else:
        get_last_quotation_no = 'QU/CU/101'
    item_code_quotation = request.POST.get('item_code_quotation',False)
    if item_code_quotation:
        data = Add_products.objects.filter(product_code = item_code_quotation)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        customer = request.POST.get('customer',False)
        attn = request.POST.get('attn',False)
        prcbasis = request.POST.get('prcbasis',False)
        leadtime = request.POST.get('leadtime',False)
        validity = request.POST.get('validity',False)
        payment = request.POST.get('payment',False)
        remarks = request.POST.get('remarks',False)
        currency = request.POST.get('currency',False)
        exchange_rate = request.POST.get('exchange_rate',False)
        follow_up = request.POST.get('follow_up',False)
        footer_remarks = request.POST.get('footer_remarks',False)
        account_id = ChartOfAccount.objects.get(account_title = customer)
        date = datetime.date.today()
        quotation_header = QuotationHeaderCustomer(quotation_no = get_last_quotation_no, date = date, attn = attn, prc_basis = prcbasis,
                                                leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
                                                exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True, footer_remarks = footer_remarks ,account_id = account_id)
        quotation_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = QuotationHeaderCustomer.objects.get(quotation_no = get_last_quotation_no)
        for value in items:
            quotation_detail = QuotationDetailCustomer(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_id = header_id)
            quotation_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'customer/new_quotation_customer.html',{'all_item_code':all_item_code,'get_last_quotation_no':get_last_quotation_no,'all_accounts':all_accounts})


def edit_quotation_customer(request,pk):
    quotation_header = QuotationHeaderCustomer.objects.filter(id = pk).first()
    quotation_detail = QuotationDetailCustomer.objects.filter(quotation_id = pk).all()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    item_code = request.POST.get('item_code',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        item_code_exist = QuotationDetailCustomer.objects.filter(item_code = item_code, quotation_id = pk).first()
        if item_code_exist:
            return HttpResponse(json.dumps({'message':"Item Already Exist"}))
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        quotation_detail.delete()
        edit_quotation = request.POST.get('customer',False)
        edit_quotation_attn = request.POST.get('attn',False)
        edit_quotation_prcbasis = request.POST.get('prcbasis',False)
        edit_quotation_leadtime = request.POST.get('leadtime',False)
        edit_quotation_validity = request.POST.get('validity',False)
        edit_quotation_payment = request.POST.get('payment',False)
        edit_quotation_remarks = request.POST.get('remarks',False)
        edit_quotation_currency_rate = request.POST.get('currency',False)
        edit_quotation_exchange_rate = request.POST.get('exchange_rate',False)
        edit_quotation_follow_up = request.POST.get('follow_up',False)
        footer_remarks = request.POST.get('footer_remarks',False)

        account_id = ChartOfAccount.objects.get(account_title = edit_quotation)

        quotation_header.attn = edit_quotation_attn
        quotation_header.prc_basis = edit_quotation_prcbasis
        quotation_header.leadtime = edit_quotation_leadtime
        quotation_header.validity = edit_quotation_validity
        quotation_header.payment = edit_quotation_payment
        quotation_header.remarks = edit_quotation_remarks
        quotation_header.currency = edit_quotation_currency_rate
        quotation_header.exchange_rate = edit_quotation_exchange_rate
        quotation_header.account_id = account_id
        quotation_header.follow_up = edit_quotation_follow_up
        quotation_header.footer_remarks = footer_remarks

        quotation_header.save();

        header_id = QuotationHeaderCustomer.objects.get(id = pk)
        items = json.loads(request.POST.get('items'))
        print(items)
        for value in items:
            quotation_detail_update = QuotationDetailCustomer(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_id = header_id)
            quotation_detail_update.save()
        return JsonResponse({"result":"success"})
    return render(request,'customer/edit_quotation_customer.html',{'quotation_header':quotation_header,'pk':pk,'quotation_detail':quotation_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts})


def print_quotation_customer(request,pk):
    lines = 0
    total_amount = 0
    company_info = Company_info.objects.all()
    image = Company_info.objects.filter(company_name = "Hamza Enterprise").first()
    header = QuotationHeaderCustomer.objects.filter(id = pk).first()
    detail = QuotationDetailCustomer.objects.filter(quotation_id = pk).all()
    for value in detail:
        lines = lines + len(value.item_description.split('\n'))
        amount = float(value.unit_price * value.quantity)
        total_amount = total_amount + amount
    print(total_amount)
    lines = lines + len(detail) + len(detail)
    total_lines = 36 - lines
    pdf = render_to_pdf('customer/quotation_customer_pdf.html', {'company_info':company_info,'image':image,'header':header, 'detail':detail,'total_lines':total_lines,'total_amount':total_amount})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Quotation_Supplier_%s.pdf" %("123")
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")



def purchase_order_customer(request):
    all_po = PoHeaderCustomer.objects.all()
    return render(request, 'customer/purchase_order_customer.html',{'all_po':all_po})


def new_purchase_order_customer(request):
    get_last_po_no = PoHeaderCustomer.objects.last()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    if get_last_po_no:
        get_last_po_no = get_last_po_no.po_no
        get_last_po_no = get_last_po_no[-3:]
        num = int(get_last_po_no)
        num = num + 1
        get_last_po_no = 'PO/CU/' + str(num)
    else:
        get_last_po_no = 'PO/CU/101'
    item_code_po = request.POST.get('item_code_po',False)
    if item_code_po:
        data = Add_products.objects.filter(product_code = item_code_po)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        customer = request.POST.get('customer',False)
        attn = request.POST.get('attn',False)
        prcbasis = request.POST.get('prcbasis',False)
        leadtime = request.POST.get('leadtime',False)
        validity = request.POST.get('validity',False)
        payment = request.POST.get('payment',False)
        remarks = request.POST.get('remarks',False)
        currency = request.POST.get('currency',False)
        exchange_rate = request.POST.get('exchange_rate',False)
        follow_up = request.POST.get('follow_up',False)
        footer_remarks = request.POST.get('footer_remarks',False)
        account_id = ChartOfAccount.objects.get(account_title = customer)

        date = datetime.date.today()
        po_header = PoHeaderCustomer(po_no = get_last_po_no, date = date, attn = attn, prc_basis = prcbasis,
                                                leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
                                                exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True, footer_remarks = footer_remarks ,account_id = account_id)
        po_header.save()
        items = json.loads(request.POST.get('items'))
        print(items)
        header_id = PoHeaderCustomer.objects.get(po_no = get_last_po_no)
        for value in items:
            po_detail = PoDetailCustomer(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_no = "to be define" ,po_id = header_id)
            po_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'customer/new_purchase_order_customer.html',{'get_last_po_no':get_last_po_no,'all_item_code':all_item_code, 'all_accounts':all_accounts})


def edit_purchase_order_customer(request,pk):
    po_header = PoHeaderCustomer.objects.filter(id = pk).first()
    po_detail = PoDetailCustomer.objects.filter(po_id = pk).all()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    item_code = request.POST.get('item_code',False)
    print(item_code)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        item_code_exist = PoDetailCustomer.objects.filter(item_code = item_code, po_id = pk).first()
        if item_code_exist:
            return HttpResponse(json.dumps({'message':"Item Already Exist"}))
            print(data)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        po_detail.delete()

        edit_po_customer = request.POST.get('customer',False)
        edit_po_attn = request.POST.get('attn',False)
        edit_po_prcbasis = request.POST.get('prcbasis',False)
        edit_po_leadtime = request.POST.get('leadtime',False)
        edit_po_validity = request.POST.get('validity',False)
        edit_po_payment = request.POST.get('payment',False)
        edit_po_remarks = request.POST.get('remarks',False)
        edit_po_currency_rate = request.POST.get('currency',False)
        edit_po_exchange_rate = request.POST.get('exchange_rate',False)
        edit_po_follow_up = request.POST.get('follow_up',False)
        footer_remarks = request.POST.get('footer_remarks',False)

        account_id = ChartOfAccount.objects.get(account_title = edit_po_customer)

        po_header.attn = edit_po_attn
        po_header.prc_basis = edit_po_prcbasis
        po_header.leadtime = edit_po_leadtime
        po_header.validity = edit_po_validity
        po_header.payment = edit_po_payment
        po_header.remarks = edit_po_remarks
        po_header.currency = edit_po_currency_rate
        po_header.exchange_rate = edit_po_exchange_rate
        po_header.account_id = account_id
        po_header.follow_up = edit_po_follow_up
        po_header.footer_remarks = footer_remarks

        po_header.save();

        header_id = PoHeaderCustomer.objects.get(id = pk)
        items = json.loads(request.POST.get('items'))
        print(items)
        for value in items:
            po_detail_update = PoDetailCustomer(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], po_id = header_id)
            po_detail_update.save()
        return JsonResponse({"result":"success"})
    return render(request,'customer/edit_purchase_order_customer.html',{'po_header':po_header,'pk':pk,'po_detail':po_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts})

def print_po_customer(request,pk):
    lines = 0
    total_amount = 0
    company_info = Company_info.objects.all()
    image = Company_info.objects.filter(company_name = "Hamza Enterprise").first()
    header = PoHeaderCustomer.objects.filter(id = pk).first()
    detail = PoDetailCustomer.objects.filter(po_id = pk).all()
    for value in detail:
        lines = lines + len(value.item_description.split('\n'))
        amount = float(value.unit_price * value.quantity)
        total_amount = total_amount + amount
    print(total_amount)
    lines = lines + len(detail) + len(detail)
    total_lines = 36 - lines
    pdf = render_to_pdf('customer/po_customer_pdf.html', {'company_info':company_info,'image':image,'header':header, 'detail':detail,'total_lines':total_lines,'total_amount':total_amount})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Quotation_Supplier_%s.pdf" %("123")
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def delivery_challan_customer(request):
    all_dc = DcHeaderCustomer.objects.all()
    return render(request, 'customer/delivery_challan_customer.html',{'all_dc':all_dc})


def new_delivery_challan_customer(request):
    all_item_code = list(Add_products.objects.values('product_code'))
    get_last_dc_no = DcHeaderCustomer.objects.last()
    all_accounts = ChartOfAccount.objects.all()
    if get_last_dc_no:
        get_last_dc_no = get_last_dc_no.dc_no
        get_last_dc_no = get_last_dc_no[-3:]
        num = int(get_last_dc_no)
        num = num + 1
        get_last_dc_no = 'DC/CU/' + str(num)
    else:
        get_last_dc_no = 'DC/CU/101'
    item_code_dc = request.POST.get('item_code_dc',False)
    if item_code_dc:
        data = Add_products.objects.filter(product_code = item_code_dc)
        for value in data:
            print(value.product_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        dc_customer = request.POST.get('customer', False)
        follow_up = request.POST.get('follow_up', False)
        footer_remarks = request.POST.get('footer_remarks', False)
        account_id = ChartOfAccount.objects.get(account_title = dc_customer)
        date = datetime.date.today()
        dc_header = DcHeaderCustomer(dc_no = get_last_dc_no, date = date, follow_up = follow_up, footer_remarks = footer_remarks ,account_id = account_id)
        dc_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = DcHeaderCustomer.objects.get(dc_no = get_last_dc_no)
        for value in items:
            dc_detail = DcDetailCustomer(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"],accepted_quantity = 0, returned_quantity = 0,  unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], po_no = "to be define" ,dc_id = header_id)
            dc_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'customer/new_delivery_challan_customer.html',{'all_item_code':all_item_code,'get_last_dc_no':get_last_dc_no,'all_accounts':all_accounts})


def edit_delivery_challan_customer(request,pk):
    dc_header = DcHeaderCustomer.objects.filter(id = pk).first()
    dc_detail = DcDetailCustomer.objects.filter(dc_id = pk).all()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    item_code = request.POST.get('item_code')
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        item_code_exist = DcDetailCustomer.objects.filter(item_code = item_code, dc_id = pk).first()
        if item_code_exist:
            return HttpResponse(json.dumps({'message':"Item Already Exist"}))
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        dc_detail.delete()

        edit_dc_customer =  request.POST.get('customer')
        follow_up = request.POST.get('follow_up')
        footer_remarks = request.POST.get('footer_remarks')
        account_id = ChartOfAccount.objects.get(account_title = edit_dc_customer)
        header_id = DcHeaderCustomer.objects.get(id = pk)

        dc_header.account_id = account_id
        dc_header.follow_up = follow_up
        dc_header.footer_remarks = footer_remarks
        dc_header.save()

        items = json.loads(request.POST.get('items'))
        for value in items:
            dc_detail_update = DcDetailCustomer(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"],accepted_quantity = 0, returned_quantity = 0, unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], dc_id = header_id)
            dc_detail_update.save()
        return JsonResponse({"result":"success"})
    return render(request,'customer/edit_delivery_challan_customer.html',{'dc_header':dc_header,'pk':pk,'dc_detail':dc_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts})


def print_dc_customer(request,pk):
    lines = 0
    total_amount = 0
    company_info = Company_info.objects.all()
    image = Company_info.objects.filter(company_name = "Hamza Enterprise").first()
    header = DcHeaderCustomer.objects.filter(id = pk).first()
    detail = DcDetailCustomer.objects.filter(dc_id = pk).all()
    for value in detail:
        lines = lines + len(value.item_description.split('\n'))
        amount = float(value.unit_price * value.quantity)
        total_amount = total_amount + amount
    print(total_amount)
    lines = lines + len(detail) + len(detail)
    total_lines = 36 - lines
    pdf = render_to_pdf('customer/dc_customer_pdf.html', {'company_info':company_info,'image':image,'header':header, 'detail':detail,'total_lines':total_lines,'total_amount':total_amount})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "DC_Customer_%s.pdf" %(header.dc_no)
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def mrn_customer(request):
    all_dc = DcHeaderCustomer.objects.all()
    return render(request, 'customer/mrn_customer.html',{'all_dc':all_dc})


def edit_mrn_customer(request,pk):
    dc_header = DcHeaderCustomer.objects.filter(id=pk).first()
    dc_detail = DcDetailCustomer.objects.filter(dc_id=pk).all()
    if request.method == 'POST':
        follow_up = request.POST.get('follow_up', False)
        dc_header.follow_up = follow_up
        dc_header.save()
        items = json.loads(request.POST.get('items'))
        for i,value in enumerate(dc_detail):
            value.accepted_quantity = items[i]["accepted_quantity"]
            value.save()
        return JsonResponse({"result":"success"})
    return render(request, 'customer/edit_mrn_customer.html',{'dc_header':dc_header,'dc_detail':dc_detail,'pk':pk})
