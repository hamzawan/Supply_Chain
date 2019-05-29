from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import (RfqSupplierHeader,RfqSupplierDetail,
                    QuotationHeaderSupplier, QuotationDetailSupplier,
                    PoHeaderSupplier, PoDetailSupplier,
                    DcHeaderSupplier, DcDetailSupplier,
                    Company_info)
from inventory.models import Add_products
from transaction.models import ChartOfAccount
from django.core import serializers
from django.forms.models import model_to_dict
import json
import datetime
from django.db import IntegrityError
from django.conf import settings
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template

def home(request):
    return render(request,'supplier/index.html')

def rfq_supplier(request):
    all_rfq = RfqSupplierHeader.objects.all()
    return render(request, 'supplier/rfq_supplier.html',{'all_rfq':all_rfq})

def new_rfq_supplier(request):
    get_last_rfq_no = RfqSupplierHeader.objects.last()
    all_item_code = list(Add_products.objects.values('product_code'))
    if get_last_rfq_no:
        get_last_rfq_no = get_last_rfq_no.rfq_no
        get_last_rfq_no = get_last_rfq_no[-3:]
        num = int(get_last_rfq_no)
        num = num + 1
        get_last_rfq_no = 'RFQ/SP/' + str(num)
    else:
        get_last_rfq_no = 'RFQ/SP/101'
    all_accounts = ChartOfAccount.objects.all()
    item_code = request.POST.get('item_code',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        for value in data:
            print(value.product_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        supplier = request.POST.get('supplier',False)
        attn = request.POST.get('attn',False)
        follow_up = request.POST.get('follow_up',False)
        items = json.loads(request.POST.get('items'))
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        print(account_id.account_title)
        date = datetime.date.today()
        rfq_header = RfqSupplierHeader(rfq_no = get_last_rfq_no, date = date , attn = attn, follow_up = follow_up, account_id = account_id)
        rfq_header.save()
        header_id = RfqSupplierHeader.objects.get(rfq_no=get_last_rfq_no)
        for value in items:
            rfq_detail = RfqSupplierDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], rfq_id = header_id)
            rfq_detail.save()
        return JsonResponse({"result": "success"})
    return render(request,'supplier/new_rfq_supplier.html',{'get_last_rfq_no':get_last_rfq_no, 'all_item_code':all_item_code, 'all_accounts':all_accounts})


def edit_rfq_supplier(request,pk):
    rfq_header = RfqSupplierHeader.objects.filter(id = pk).first()
    rfq_detail = RfqSupplierDetail.objects.filter(rfq_id = pk).all()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    try:
        item_code = request.POST.get('item_code',False)
        print(item_code)
        if item_code:
            data = Add_products.objects.filter(product_code = item_code)
            item_code_exist = RfqSupplierDetail.objects.filter(item_code = item_code, rfq_id = pk).first()
            if item_code_exist:
                return HttpResponse(json.dumps({'message':"Item Already Exist"}))
            row = serializers.serialize('json',data)
            return HttpResponse(json.dumps({'row':row}))
        if request.method == 'POST':
            rfq_detail.delete()
            edit_rfq_supplier_name = request.POST.get('edit_rfq_supplier_name',False)
            edit_rfq_attn = request.POST.get('edit_rfq_attn',False)
            edit_rfq_follow_up = request.POST.get('edit_rfq_follow_up',False)
            account_id = ChartOfAccount.objects.get(account_title = edit_rfq_supplier_name)
            rfq_header.attn = edit_rfq_attn
            rfq_header.follow_up = edit_rfq_follow_up
            rfq_header.account_id = account_id
            rfq_header.save();
            header_id = RfqSupplierHeader.objects.get(id = pk)
            items = json.loads(request.POST.get('items'))
            for value in items:
                rfq_detail_update = RfqSupplierDetail(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], unit = value["unit"], rfq_id = header_id)
                rfq_detail_update.save()
            return JsonResponse({"result":"success"})
    except IntegrityError:
        print("Data Already Exist")
    return render(request,'supplier/edit_rfq_supplier.html',{'rfq_header':rfq_header,'pk':pk,'rfq_detail':rfq_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts})


def quotation_supplier(request):
    all_quotation = QuotationHeaderSupplier.objects.all()
    return render(request, 'supplier/quotation_supplier.html',{'all_quotation':all_quotation})


def new_quotation_supplier(request):
    get_last_quotation_no = QuotationHeaderSupplier.objects.last()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    if get_last_quotation_no:
        get_last_quotation_no = get_last_quotation_no.quotation_no
        get_last_quotation_no = get_last_quotation_no[-3:]
        num = int(get_last_quotation_no)
        num = num + 1
        get_last_quotation_no = 'QU/SP/' + str(num)
    else:
        get_last_quotation_no = 'QU/SP/101'
    item_code_quotation = request.POST.get('item_code_quotation',False)
    if item_code_quotation:
        data = Add_products.objects.filter(product_code = item_code_quotation)
        for value in data:
            print(value.product_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        supplier = request.POST.get('supplier',False)
        attn = request.POST.get('attn',False)
        prcbasis = request.POST.get('prcbasis',False)
        leadtime = request.POST.get('leadtime',False)
        validity = request.POST.get('validity',False)
        payment = request.POST.get('payment',False)
        remarks = request.POST.get('remarks',False)
        currency = request.POST.get('currency',False)
        exchange_rate = request.POST.get('exchange_rate',False)
        follow_up = request.POST.get('follow_up',False)
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        date = datetime.date.today()
        quotation_header = QuotationHeaderSupplier(quotation_no = get_last_quotation_no, date = date, attn = attn, prc_basis = prcbasis,
                                                leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
                                                exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True, account_id = account_id)
        quotation_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = QuotationHeaderSupplier.objects.get(quotation_no = get_last_quotation_no)
        for value in items:
            quotation_detail = QuotationDetailSupplier(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_id = header_id)
            quotation_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'supplier/new_quotation_supplier.html',{'all_item_code':all_item_code,'get_last_quotation_no':get_last_quotation_no,'all_accounts':all_accounts})


def edit_quotation_supplier(request,pk):
    quotation_header = QuotationHeaderSupplier.objects.filter(id = pk).first()
    quotation_detail = QuotationDetailSupplier.objects.filter(quotation_id = pk).all()
    all_accounts = ChartOfAccount.objects.all()
    print(quotation_detail)
    all_item_code = list(Add_products.objects.values('product_code'))
    item_code = request.POST.get('item_code',False)
    print(item_code)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        item_code_exist = QuotationDetailSupplier.objects.filter(item_code = item_code, quotation_id = pk).first()
        if item_code_exist:
            return HttpResponse(json.dumps({'message':"Item Already Exist"}))
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        quotation_detail.delete()
        edit_supplier = request.POST.get('supplier',False)
        edit_quotation_attn = request.POST.get('attn',False)
        edit_quotation_prcbasis = request.POST.get('prcbasis',False)
        edit_quotation_leadtime = request.POST.get('leadtime',False)
        edit_quotation_validity = request.POST.get('validity',False)
        edit_quotation_payment = request.POST.get('payment',False)
        edit_quotation_remarks = request.POST.get('remarks',False)
        edit_quotation_currency_rate = request.POST.get('currency',False)
        edit_quotation_exchange_rate = request.POST.get('exchange_rate',False)
        edit_quotation_follow_up = request.POST.get('follow_up',False)

        account_id = ChartOfAccount.objects.get(account_title = edit_supplier)

        quotation_header.attn = edit_quotation_attn
        quotation_header.prc_basis = edit_quotation_prcbasis
        quotation_header.leadtime = edit_quotation_leadtime
        quotation_header.validity = edit_quotation_validity
        quotation_header.payment = edit_quotation_payment
        quotation_header.remarks = edit_quotation_remarks
        quotation_header.currency = edit_quotation_currency_rate
        quotation_header.exchange_rate = edit_quotation_exchange_rate
        quotation_header.account_id = account_id

        quotation_header.save();

        header_id = QuotationHeaderSupplier.objects.get(id = pk)
        items = json.loads(request.POST.get('items'))
        print(items)
        for value in items:
            quotation_detail_update = QuotationDetailSupplier(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_id = header_id)
            quotation_detail_update.save()
        return JsonResponse({"result":"success"})
    return render(request,'supplier/edit_quotation_supplier.html',{'quotation_header':quotation_header,'pk':pk,'quotation_detail':quotation_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts})


def purchase_order_supplier(request):
    all_po = PoHeaderSupplier.objects.all()
    return render(request, 'supplier/purchase_order_supplier.html',{'all_po':all_po})


def new_purchase_order_supplier(request):
    get_last_po_no = PoHeaderSupplier.objects.last()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    if get_last_po_no:
        get_last_po_no = get_last_po_no.po_no
        get_last_po_no = get_last_po_no[-3:]
        num = int(get_last_po_no)
        num = num + 1
        get_last_po_no = 'PO/SP/' + str(num)
    else:
        get_last_po_no = 'PO/SP/101'
    item_code_po = request.POST.get('item_code_po',False)
    if item_code_po:
        data = Add_products.objects.filter(product_code = item_code_po)
        for value in data:
            print(value.product_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        supplier = request.POST.get('supplier',False)
        attn = request.POST.get('attn',False)
        prcbasis = request.POST.get('prcbasis',False)
        leadtime = request.POST.get('leadtime',False)
        validity = request.POST.get('validity',False)
        payment = request.POST.get('payment',False)
        remarks = request.POST.get('remarks',False)
        currency = request.POST.get('currency',False)
        exchange_rate = request.POST.get('exchange_rate',False)
        follow_up = request.POST.get('follow_up',False)
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        date = datetime.date.today()
        po_header = PoHeaderSupplier(po_no = get_last_po_no, date = date, attn = attn, prc_basis = prcbasis,
                                                leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
                                                exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True, account_id = account_id)
        po_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = PoHeaderSupplier.objects.get(po_no = get_last_po_no)
        for value in items:
            po_detail = PoDetailSupplier(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_no = "to be define" ,po_id = header_id)
            po_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'supplier/new_purchase_order_supplier.html',{'all_item_code':all_item_code,'get_last_po_no':get_last_po_no, 'all_accounts': all_accounts})


def edit_purchase_order_supplier(request,pk):
    po_header = PoHeaderSupplier.objects.filter(id = pk).first()
    po_detail = PoDetailSupplier.objects.filter(po_id = pk).all()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    item_code = request.POST.get('item_code')
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        item_code_exist = PoDetailSupplier.objects.filter(item_code = item_code, po_id = pk).first()
        if item_code_exist:
            return HttpResponse(json.dumps({'message':"Item Already Exist"}))
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        po_detail.delete()
        edit_po_supplier = request.POST.get('supplier',False)
        edit_po_attn = request.POST.get('attn',False)
        edit_po_prcbasis = request.POST.get('prcbasis',False)
        edit_po_leadtime = request.POST.get('leadtime',False)
        edit_po_validity = request.POST.get('validity',False)
        edit_po_payment = request.POST.get('payment',False)
        edit_po_remarks = request.POST.get('remarks',False)
        edit_po_currency_rate = request.POST.get('currency',False)
        edit_po_exchange_rate = request.POST.get('exchange_rate',False)
        edit_po_follow_up = request.POST.get('follow_up',False)

        account_id = ChartOfAccount.objects.get(account_title = edit_po_supplier)

        po_header.attn = edit_po_attn
        po_header.prc_basis = edit_po_prcbasis
        po_header.leadtime = edit_po_leadtime
        po_header.validity = edit_po_validity
        po_header.payment = edit_po_payment
        po_header.remarks = edit_po_remarks
        po_header.currency = edit_po_currency_rate
        po_header.exchange_rate = edit_po_exchange_rate
        po_header.account_id = account_id
        po_header.save();

        header_id = PoHeaderSupplier.objects.get(id = pk)
        items = json.loads(request.POST.get('items'))
        for value in items:
            po_detail_update = PoDetailSupplier(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], po_id = header_id)
            po_detail_update.save()
        return JsonResponse({"result":"success"})
    return render(request,'supplier/edit_purchase_order_supplier.html',{'po_header':po_header,'pk':pk,'po_detail':po_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts})


def delivery_challan_supplier(request):
    all_dc = DcHeaderSupplier.objects.all()
    return render(request, 'supplier/delivery_challan_supplier.html',{'all_dc':all_dc})


def new_delivery_challan_supplier(request):
    all_item_code = list(Add_products.objects.values('product_code'))
    get_last_dc_no = DcHeaderSupplier.objects.last()
    all_accounts = ChartOfAccount.objects.all()
    if get_last_dc_no:
        get_last_dc_no = get_last_dc_no.dc_no
        get_last_dc_no = get_last_dc_no[-3:]
        num = int(get_last_dc_no)
        num = num + 1
        get_last_dc_no = 'DC/SP/' + str(num)
    else:
        get_last_dc_no = 'DC/SP/101'
    item_code_dc = request.POST.get('item_code_dc',False)
    if item_code_dc:
        data = Add_products.objects.filter(product_code = item_code_dc)
        for value in data:
            print(value.product_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        dc_supplier = request.POST.get('supplier')
        account_id = ChartOfAccount.objects.get(account_title = dc_supplier)
        date = datetime.date.today()
        dc_header = DcHeaderSupplier(dc_no = get_last_dc_no, date = date, account_id = account_id)
        dc_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = DcHeaderSupplier.objects.get(dc_no = get_last_dc_no)
        for value in items:
            dc_detail = DcDetailSupplier(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"],
                                            quantity = value["quantity"],accepted_quantity = 0, returned_quantity = 0,  unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], po_no = "to be define" ,dc_id = header_id)
            dc_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'supplier/new_delivery_challan_supplier.html',{'all_item_code':all_item_code,'get_last_dc_no':get_last_dc_no,'all_accounts':all_accounts})


def edit_delivery_challan_supplier(request,pk):
    dc_header = DcHeaderSupplier.objects.filter(id = pk).first()
    dc_detail = DcDetailSupplier.objects.filter(dc_id = pk).all()
    all_accounts = ChartOfAccount.objects.all()
    all_item_code = list(Add_products.objects.values('product_code'))
    item_code = request.POST.get('item_code')
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        item_code_exist = DcDetailSupplier.objects.filter(item_code = item_code, dc_id = pk).first()
        if item_code_exist:
            return HttpResponse(json.dumps({'message':"Item Already Exist"}))
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        dc_detail.delete()
        dc_supplier = request.POST.get('supplier')
        account_id = ChartOfAccount.objects.get(account_title = dc_supplier)
        dc_header.account_id = account_id
        dc_header.save()
        header_id = DcHeaderSupplier.objects.get(id = pk)
        items = json.loads(request.POST.get('items'))
        for value in items:
            dc_detail_update = DcDetailSupplier(item_code = value["item_code"], item_name = value["item_name"], item_description = value["item_description"], quantity = value["quantity"],accepted_quantity = 0, returned_quantity = 0, unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], dc_id = header_id)
            dc_detail_update.save()
        return JsonResponse({"result":"success"})
    return render(request,'supplier/edit_delivery_challan_supplier.html',{'dc_header':dc_header,'pk':pk,'dc_detail':dc_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts})


def mrn_supplier(request):
    all_dc = DcHeaderSupplier.objects.all()
    return render(request, 'supplier/mrn_supplier.html',{'all_dc':all_dc})


def edit_mrn_supplier(request,pk):
    dc_header = DcHeaderSupplier.objects.filter(id=pk).first()
    dc_detail = DcDetailSupplier.objects.filter(dc_id=pk).all()
    if request.method == 'POST':
        items = json.loads(request.POST.get('items'))
        for i,value in enumerate(dc_detail):
            value.accepted_quantity = items[i]["accepted_quantity"]
            value.save()
        return JsonResponse({"result":"success"})
    return render(request, 'supplier/edit_mrn_supplier.html',{'dc_header':dc_header,'dc_detail':dc_detail,'pk':pk})


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        company_info = Company_info.objects.all()
        image = Company_info.objects.filter(company_name = "Hamza Enterprise").first()
        pdf = render_to_pdf('supplier/rfq_pdf.html', {'company_info':company_info,'image':image})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Rfq_Supplier_%s.pdf" %("123")
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
