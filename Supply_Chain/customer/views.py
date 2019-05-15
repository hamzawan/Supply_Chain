from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import (RfqCustomerHeader, RfqCustomerDetail,
                    QuotationHeaderCustomer, QuotationDetailCustomer,
                    PoHeaderCustomer, PoDetailCustomer,
                    DcHeaderCustomer, DcDetailCustomer)
from django.core import serializers
from django.forms.models import model_to_dict
import json
import datetime


def rfq_customer(request):
    all_rfq = RfqCustomerHeader.objects.all()
    return render(request, 'customer/rfq_customer.html',{'all_rfq':all_rfq})


def new_rfq_customer(request):
    get_last_rfq_no = RfqCustomerHeader.objects.last()
    if get_last_rfq_no:
        get_last_rfq_no = get_last_rfq_no.rfq_no
        get_last_rfq_no = get_last_rfq_no[-3:]
        num = int(get_last_rfq_no)
        num = num + 1
        get_last_rfq_no = 'RFQ/CU/' + str(num)
    else:
        get_last_rfq_no = 'RFQ/CU/101'
    if request.method == 'POST':
        attn = request.POST.get('attn',False)
        follow_up = request.POST.get('follow_up',False)
        items = json.loads(request.POST.get('items'))
        print(items)
        date = datetime.date.today()
        rfq_header = RfqCustomerHeader(rfq_no = get_last_rfq_no, date = date , attn = attn, follow_up = follow_up)
        rfq_header.save()
        header_id = RfqCustomerHeader.objects.get(rfq_no=get_last_rfq_no)
        for value in items:
            rfq_detail = RfqCustomerDetail(item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], rfq_id = header_id)
            rfq_detail.save()
        return JsonResponse({"result": "success"})
    return render(request,'customer/new_rfq_customer.html',{'get_last_rfq_no':get_last_rfq_no})


def edit_rfq_customer(request,pk):
    rfq_header = RfqCustomerHeader.objects.filter(id = pk).first()
    rfq_detail = RfqCustomerDetail.objects.filter(rfq_id = pk).all()
    print(rfq_detail)
    if request.method == 'POST':
        items = json.loads(request.POST.get('items'))
        print(rfq_detail)
        # for i, value in enumerate(rfq_detail):
        #     value.item_name = items[i]["item_name"]
        #     value.item_description = items[i]["item_description"]
        #     value.unit = items[i]["unit"]
        #     value.quantity = items[i]["quantity"]
        #     value.save()

        return JsonResponse({"result":"success"})
    return render(request,'customer/edit_rfq_customer.html',{'rfq_header':rfq_header,'pk':pk,'rfq_detail':rfq_detail})


def quotation_customer(request):
    return render(request, 'customer/quotation_customer.html')


def new_quotation_customer(request):
    all_rfq = list(RfqCustomerHeader.objects.values('rfq_no'))
    get_last_quotation_no = QuotationHeaderCustomer.objects.last()
    if get_last_quotation_no:
        get_last_quotation_no = get_last_quotation_no.quotation_no
        get_last_quotation_no = get_last_quotation_no[-3:]
        num = int(get_last_quotation_no)
        num = num + 1
        get_last_quotation_no = 'QU/CU/' + str(num)
    else:
        get_last_quotation_no = 'QU/CU/101'
    rfq_no = request.POST.get('rfq_no',False)
    if rfq_no:
        fk = RfqCustomerHeader.objects.get(rfq_no = rfq_no)
        data = RfqCustomerDetail.objects.filter(rfq_id = fk)
        for value in data:
            print(value.item_name)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        attn = request.POST.get('attn',False)
        prcbasis = request.POST.get('prcbasis',False)
        leadtime = request.POST.get('leadtime',False)
        validity = request.POST.get('validity',False)
        payment = request.POST.get('payment',False)
        remarks = request.POST.get('remarks',False)
        currency = request.POST.get('currency',False)
        exchange_rate = request.POST.get('exchange_rate',False)
        follow_up = request.POST.get('follow_up',False)
        date = datetime.date.today()
        quotation_header = QuotationHeaderCustomer(quotation_no = get_last_quotation_no, date = date, attn = attn, prc_basis = prcbasis,
                                                leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
                                                exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True)
        quotation_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = QuotationHeaderCustomer.objects.get(quotation_no = get_last_quotation_no)
        for value in items:
            quotation_detail = QuotationDetailCustomer(item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_id = header_id)
            quotation_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'customer/new_quotation_customer.html',{'all_rfq':all_rfq,'get_last_quotation_no':get_last_quotation_no})


def edit_quotation_customer(request):
    return render(request, 'customer/edit_quotation_customer.html')


def purchase_order_customer(request):
    return render(request, 'customer/purchase_order_customer.html')


def new_purchase_order_customer(request):
    all_quotation = list(QuotationHeaderCustomer.objects.values('quotation_no'))
    get_last_po_no = PoHeaderCustomer.objects.last()
    if get_last_po_no:
        get_last_po_no = get_last_po_no.po_no
        get_last_po_no = get_last_po_no[-3:]
        num = int(get_last_po_no)
        num = num + 1
        get_last_po_no = 'PO/CU/' + str(num)
    else:
        get_last_po_no = 'PO/CU/101'
    quotation_no = request.POST.get('quotation_no',False)
    if quotation_no:
        fk = QuotationHeaderCustomer.objects.get(quotation_no = quotation_no)
        data = QuotationDetailCustomer.objects.filter(quotation_id = fk)
        print(data)
        for value in data:
            print(value.quotation_id)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row, 'quotation_no':quotation_no}))
    if request.method == 'POST':
        attn = request.POST.get('attn',False)
        prcbasis = request.POST.get('prcbasis',False)
        leadtime = request.POST.get('leadtime',False)
        validity = request.POST.get('validity',False)
        payment = request.POST.get('payment',False)
        remarks = request.POST.get('remarks',False)
        currency = request.POST.get('currency',False)
        exchange_rate = request.POST.get('exchange_rate',False)
        follow_up = request.POST.get('follow_up',False)
        date = datetime.date.today()
        po_header = PoHeaderCustomer(po_no = get_last_po_no, date = date, attn = attn, prc_basis = prcbasis,
                                                leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
                                                exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True)
        po_header.save()
        items = json.loads(request.POST.get('items'))
        print(items)
        header_id = PoHeaderCustomer.objects.get(po_no = get_last_po_no)
        for value in items:
            po_detail = PoDetailCustomer(item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_no = value["quotation_no"] ,po_id = header_id)
            po_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'customer/new_purchase_order_customer.html',{'all_quotation':all_quotation,'get_last_po_no':get_last_po_no})


def edit_purchase_order_customer(request):
    return render(request, 'customer/edit_purchase_order_customer.html')


def delivery_challan_customer(request):
    return render(request, 'customer/delivery_challan_customer.html')


def new_delivery_challan_customer(request):
    all_po = list(PoHeaderCustomer.objects.values('po_no'))
    get_last_dc_no = DcHeaderCustomer.objects.last()
    if get_last_dc_no:
        get_last_dc_no = get_last_dc_no.dc_no
        get_last_dc_no = get_last_dc_no[-3:]
        num = int(get_last_dc_no)
        num = num + 1
        get_last_dc_no = 'DC/CU/' + str(num)
    else:
        get_last_dc_no = 'DC/CU/101'
    po_no = request.POST.get('po_no',False)
    if po_no:
        fk = PoHeaderCustomer.objects.get(po_no = po_no)
        data = PoDetailCustomer.objects.filter(po_id = fk)
        print(data)
        for value in data:
            print(value.po_id)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row, 'po_no':po_no}))
    if request.method == 'POST':
        date = datetime.date.today()
        dc_header = DcHeaderCustomer(dc_no = get_last_dc_no, date = date, mrn_status = "Pending")
        dc_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = DcHeaderCustomer.objects.get(dc_no = get_last_dc_no)
        for value in items:
            dc_detail = DcDetailCustomer(item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], po_no = value["po_no"] ,dc_id = header_id)
            dc_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'customer/new_delivery_challan_customer.html',{'all_po':all_po,'get_last_dc_no':get_last_dc_no})


def edit_delivery_challan_customer(request):
    return render(request, 'customer/edit_delivery_challan_customer.html')


def mrn_customer(request):
    all_dc = DcHeaderCustomer.objects.all()
    return render(request, 'customer/mrn_customer.html',{'all_dc':all_dc})


def edit_mrn_customer(request,pk):
    return render(request, 'customer/edit_mrn_customer.html')
