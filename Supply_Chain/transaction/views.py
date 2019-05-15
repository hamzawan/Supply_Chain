from django.shortcuts import render
from django.http import HttpResponse
from supplier.models import DcHeaderSupplier, DcDetailSupplier
from django.core import serializers
from django.db.models import Q
import json


def purchase(request):
    return render(request, 'transaction/purchase.html')


def new_purchase(request):
    all_item_code = DcDetailSupplier.objects.filter(~Q(accepted_quantity = 0))
    print(all_item_code)
    for value in all_item_code:
        print(value.item_code)
    # get_last_quotation_no = QuotationHeaderSupplier.objects.last()
    # if get_last_quotation_no:
    #     get_last_quotation_no = get_last_quotation_no.quotation_no
    #     get_last_quotation_no = get_last_quotation_no[-3:]
    #     num = int(get_last_quotation_no)
    #     num = num + 1
    #     get_last_quotation_no = 'QU/SP/' + str(num)
    # else:
    #     get_last_quotation_no = 'QU/SP/101'
    item_code = request.POST.get('item_code_purchase',False)
    if item_code:
        data = DcDetailSupplier.objects.filter(item_code = item_code)
        for value in data:
            print(value.item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    # if request.method == 'POST':
    #     attn = request.POST.get('attn',False)
    #     prcbasis = request.POST.get('prcbasis',False)
    #     leadtime = request.POST.get('leadtime',False)
    #     validity = request.POST.get('validity',False)
    #     payment = request.POST.get('payment',False)
    #     remarks = request.POST.get('remarks',False)
    #     currency = request.POST.get('currency',False)
    #     exchange_rate = request.POST.get('exchange_rate',False)
    #     follow_up = request.POST.get('follow_up',False)
    #     date = datetime.date.today()
    #     quotation_header = QuotationHeaderSupplier(quotation_no = get_last_quotation_no, date = date, attn = attn, prc_basis = prcbasis,
    #                                             leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
    #                                             exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True)
    #     quotation_header.save()
    #     items = json.loads(request.POST.get('items'))
    #     header_id = QuotationHeaderSupplier.objects.get(quotation_no = get_last_quotation_no)
    #     for value in items:
    #         quotation_detail = QuotationDetailSupplier(item_name = value["item_name"], item_description = value["item_description"],
    #                                         quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_id = header_id)
    #         quotation_detail.save()
    #     return JsonResponse({'result':'success'})
    return render(request, 'transaction/new_purchase.html',{'all_item_code':all_item_code})
