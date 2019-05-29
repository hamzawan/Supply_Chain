from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import (Add_products)
from transaction.models import (PurchaseDetail, SaleDetail)
from itertools import chain
import json
from django.db import connection

def item_stock(request):
    cursor = connection.cursor()
    cursor.execute('''Select item_code, item_name,Item_description,Unit,SUM(quantity) As qty From (
Select 'Opening Stock' As TranType,Product_Code As Item_Code,Product_Name As Item_name,Product_desc As Item_description,Unit As unit,Opening_Stock as Quantity From inventory_add_products
union All
Select 'Purchase' As TranType,Item_Code,Item_name,Item_description,unit,Quantity From transaction_purchasedetail
union All
Select 'Purchase Return' As TranType,Item_Code,Item_name,Item_description,unit,Quantity * -1 From transaction_purchasereturndetail
union All
Select 'Sale' As TranType,Item_Code,Item_name,Item_description,unit,Quantity * -1 From transaction_saledetail
union All
Select 'Sale Return' As TranType,Item_Code,Item_name,Item_description,unit,Quantity  From transaction_salereturndetail
) As tblTemp
Group by Item_Code''')
    row = cursor.fetchall()
    return render(request, 'inventory/item_stock.html',{'row':row})

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
        opening_stock = request.POST.get('opening_stock',False)
        type = request.POST.get('type',False)
        size = request.POST.get('size',False)
        return JsonResponse({"product_name":product_name,"type":type,"size":size,"product_desc": product_desc,'opening_stock':opening_stock})
    if request.method == 'POST':
        items = json.loads(request.POST.get('items'))
        for value in items:
            type = value["type"][:3]
            size = value["size"][:3]
            item_code = type+"-"+size+"-"+str(serial_no)
            new_products = Add_products(product_code = item_code, product_name = value["item_name"], product_desc = value["item_desc"], opening_stock = value["opening_stock"])
            new_products.save()
            serial_no = serial_no + 1
        return JsonResponse({"result":"success"})
    return render(request, 'inventory/add_product.html')
