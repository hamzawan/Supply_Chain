from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import (RfqSupplierHeader,RfqSupplierDetail,
                    QuotationHeaderSupplier, QuotationDetailSupplier,
                    PoHeaderSupplier, PoDetailSupplier,
                    DcHeaderSupplier, DcDetailSupplier)
from django.core import serializers
from django.forms.models import model_to_dict
import json
import datetime


def home(request):
    return render(request,'supplier/index.html')

def rfq_supplier(request):
    all_rfq = RfqSupplierHeader.objects.all()
    return render(request, 'supplier/rfq_supplier.html',{'all_rfq':all_rfq})


def new_rfq_supplier(request):
    get_last_rfq_no = RfqSupplierHeader.objects.last()
    if get_last_rfq_no:
        get_last_rfq_no = get_last_rfq_no.rfq_no
        get_last_rfq_no = get_last_rfq_no[-3:]
        num = int(get_last_rfq_no)
        num = num + 1
        get_last_rfq_no = 'RFQ/SP/' + str(num)
    else:
        get_last_rfq_no = 'RFQ/SP/101'
    if request.method == 'POST':
        attn = request.POST.get('attn',False)
        follow_up = request.POST.get('follow_up',False)
        items = json.loads(request.POST.get('items'))
        date = datetime.date.today()
        rfq_header = RfqSupplierHeader(rfq_no = get_last_rfq_no, date = date , attn = attn, follow_up = follow_up)
        rfq_header.save()
        header_id = RfqSupplierHeader.objects.get(rfq_no=get_last_rfq_no)
        for value in items:
            rfq_detail = RfqSupplierDetail(item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], rfq_id = header_id)
            rfq_detail.save()
        return JsonResponse({"result": "success"})
    return render(request,'supplier/new_rfq_supplier.html',{'get_last_rfq_no':get_last_rfq_no})


def edit_rfq_supplier(request,pk):
    rfq_header = RfqSupplierHeader.objects.filter(id = pk).first()
    rfq_detail = RfqSupplierDetail.objects.filter(rfq_id = pk).all()
    if request.method == 'POST':
        items = json.loads(request.POST.get('items'))
        for i, value in enumerate(rfq_detail):
            value.item_name = items[i]["item_name"]
            value.item_description = items[i]["item_description"]
            value.unit = items[i]["unit"]
            value.quantity = items[i]["quantity"]
            value.save()
        return JsonResponse({"result":"success"})
    return render(request,'supplier/edit_rfq_supplier.html',{'rfq_header':rfq_header,'pk':pk,'rfq_detail':rfq_detail})

def quotation_supplier(request):
    all_quotation = QuotationHeaderSupplier.objects.all()
    return render(request, 'supplier/quotation_supplier.html',{'all_quotation':all_quotation})


def new_quotation_supplier(request):
    all_rfq = list(RfqSupplierHeader.objects.values('rfq_no'))
    get_last_quotation_no = QuotationHeaderSupplier.objects.last()
    if get_last_quotation_no:
        get_last_quotation_no = get_last_quotation_no.quotation_no
        get_last_quotation_no = get_last_quotation_no[-3:]
        num = int(get_last_quotation_no)
        num = num + 1
        get_last_quotation_no = 'QU/SP/' + str(num)
    else:
        get_last_quotation_no = 'QU/SP/101'
    rfq_no = request.POST.get('rfq_no',False)
    if rfq_no:
        fk = RfqSupplierHeader.objects.get(rfq_no = rfq_no)
        data = RfqSupplierDetail.objects.filter(rfq_id = fk)
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
        quotation_header = QuotationHeaderSupplier(quotation_no = get_last_quotation_no, date = date, attn = attn, prc_basis = prcbasis,
                                                leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
                                                exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True)
        quotation_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = QuotationHeaderSupplier.objects.get(quotation_no = get_last_quotation_no)
        for value in items:
            quotation_detail = QuotationDetailSupplier(item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_id = header_id)
            quotation_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'supplier/new_quotation_supplier.html',{'all_rfq':all_rfq,'get_last_quotation_no':get_last_quotation_no})


def edit_quotation_supplier(request,pk):
    quotation_header = QuotationHeaderSupplier.objects.filter(id = pk).first()
    quotation_detail = QuotationDetailSupplier.objects.filter(quotation_id = pk).all()
    return render(request, 'supplier/edit_quotation_supplier.html',{'quotation_header':quotation_header,'quotation_detail':quotation_detail})


def purchase_order_supplier(request):
    all_po = PoHeaderSupplier.objects.all()
    return render(request, 'supplier/purchase_order_supplier.html',{'all_po':all_po})


def new_purchase_order_supplier(request):
    all_quotation = list(QuotationHeaderSupplier.objects.values('quotation_no'))
    get_last_po_no = PoHeaderSupplier.objects.last()
    if get_last_po_no:
        get_last_po_no = get_last_po_no.po_no
        get_last_po_no = get_last_po_no[-3:]
        num = int(get_last_po_no)
        num = num + 1
        get_last_po_no = 'PO/SP/' + str(num)
    else:
        get_last_po_no = 'PO/SP/101'
    quotation_no = request.POST.get('quotation_no',False)
    if quotation_no:
        fk = QuotationHeaderSupplier.objects.get(quotation_no = quotation_no)
        data = QuotationDetailSupplier.objects.filter(quotation_id = fk)
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
        po_header = PoHeaderSupplier(po_no = get_last_po_no, date = date, attn = attn, prc_basis = prcbasis,
                                                leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
                                                exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True)
        po_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = PoHeaderSupplier.objects.get(po_no = get_last_po_no)
        for value in items:
            po_detail = PoDetailSupplier(item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_no = value["quotation_no"] ,po_id = header_id)
            po_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'supplier/new_purchase_order_supplier.html',{'all_quotation':all_quotation,'get_last_po_no':get_last_po_no})


def edit_purchase_order_supplier(request,pk):
    po_header = PoHeaderSupplier.objects.filter(id=pk).first()
    po_detail = PoDetailSupplier.objects.filter(po_id=pk).all()
    return render(request, 'supplier/edit_purchase_order_supplier.html',{'po_header':po_header, 'po_detail':po_detail})


def delivery_challan_supplier(request):
    all_dc = DcHeaderSupplier.objects.all()
    return render(request, 'supplier/delivery_challan_supplier.html',{'all_dc':all_dc})


def new_delivery_challan_supplier(request):
    all_po = list(PoHeaderSupplier.objects.values('po_no'))
    get_last_dc_no = DcHeaderSupplier.objects.last()
    if get_last_dc_no:
        get_last_dc_no = get_last_dc_no.dc_no
        get_last_dc_no = get_last_dc_no[-3:]
        num = int(get_last_dc_no)
        num = num + 1
        get_last_dc_no = 'DC/SP/' + str(num)
    else:
        get_last_dc_no = 'DC/SP/101'
    po_no = request.POST.get('po_no',False)
    if po_no:
        fk = PoHeaderSupplier.objects.get(po_no = po_no)
        data = PoDetailSupplier.objects.filter(po_id = fk)
        print(data)
        for value in data:
            print(value.po_id)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row, 'po_no':po_no}))
    if request.method == 'POST':
        date = datetime.date.today()
        dc_header = DcHeaderSupplier(dc_no = get_last_dc_no, date = date, mrn_status = "Pending")
        dc_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = DcHeaderSupplier.objects.get(dc_no = get_last_dc_no)
        for value in items:
            dc_detail = DcDetailSupplier(item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], po_no = value["po_no"] ,dc_id = header_id)
            dc_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'supplier/new_delivery_challan_supplier.html',{'all_po':all_po,'get_last_dc_no':get_last_dc_no})


def edit_delivery_challan_supplier(request,pk):
    dc_header = DcHeaderSupplier.objects.filter(id=pk).first()
    dc_detail = DcDetailSupplier.objects.filter(dc_id=pk).all()
    return render(request, 'supplier/edit_delivery_challan_supplier.html',{'dc_header':dc_header,'dc_detail':dc_detail})


def mrn_supplier(request):
    all_dc = DcHeaderSupplier.objects.all()
    return render(request, 'supplier/mrn_supplier.html',{'all_dc':all_dc})


def edit_mrn_supplier(request,pk):
    dc_header = DcHeaderSupplier.objects.filter(id=pk).first()
    dc_detail = DcDetailSupplier.objects.filter(dc_id=pk).all()
    print(dc_detail)
    return render(request, 'supplier/edit_mrn_supplier.html',{'dc_header':dc_header,'dc_detail':dc_detail})
