from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import (Add_products)
import json


def item_stock(request):
    
    return render(request, 'inventory/item_stock.html')

def new_item_stock(request):
    return render(request, 'inventory/new_item_stock.html')

def add_product(request):
    get_item_code = Add_products.objects.last()
    if get_item_code:
        get_item_code = get_item_code.product_code
        serial_no = get_item_code[-4:]
        serial_no = int(serial_no) + 1
    else:
        inc = 1
        serial_no = int('1001')
    product_name = request.POST.get('product_name',False)
    product_desc = request.POST.get('product_desc',False)
    type = request.POST.get('type',False)
    size = request.POST.get('size',False)
    if product_name and product_desc and type and size:
        product_name = request.POST.get('product_name',False)
        product_desc = request.POST.get('product_desc',False)
        type = request.POST.get('type',False)
        size = request.POST.get('size',False)
        return JsonResponse({"product_name":product_name,"type":type,"size":size,"product_desc": product_desc})
    if request.method == 'POST':
        items = json.loads(request.POST.get('items'))
        for value in items:
            type = value["type"][:3]
            size = value["size"][:3]
            item_code = type+"-"+size+"-"+str(serial_no)
            new_products = Add_products(product_code = item_code, product_name = value["product_name"], product_desc = value["product_desc"])
            new_products.save()
            serial_no = serial_no + 1
        return JsonResponse({"result":"success"})
    return render(request, 'inventory/add_product.html')
