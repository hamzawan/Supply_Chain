from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import (Add_products)
from transaction.models import (PurchaseDetail, SaleDetail)
from itertools import chain
import json
from django.db import connection

def item_stock(request):
    cursor = connection.cursor()
    cursor.execute('''Select itemID,Size,item_code, item_name,Item_description,Unit,Size,SUM(quantity) As qty From (
                        Select 'Opening Stock' As TranType,ID As ItemID, Size,Product_Code As Item_Code,Product_Name As Item_name,Product_desc As Item_description,Unit As unit,Opening_Stock as Quantity
                        From inventory_add_products
                        union all
                        Select 'Purchase' As TranType,P.ID As ItemID,P.Size,Item_Code,Item_name,Item_description,H.unit,Quantity
                        From transaction_purchasedetail H Inner join inventory_add_products P On H.item_code = P.product_code
                        union All
                        Select 'Purchase Return' As TranType,P.ID As ItemID,P.Size,Item_Code,Item_name,Item_description,H.unit,Quantity * -1
                        From transaction_purchasereturndetail H Inner join inventory_add_products P On H.item_code = P.product_code
                        union all
                        Select 'Sale' As TranType,P.ID AS ItemID,P.Size,Item_Code,Item_name,Item_description,H.unit,Quantity * -1
                        From transaction_saledetail H Inner join inventory_add_products P On H.item_code = P.product_code
                        union all
                        Select 'Sale Return' As TranType,P.ID AS ItemID,P.Size,Item_Code,Item_name,Item_description,H.unit,Quantity
                        From transaction_salereturndetail H Inner join inventory_add_products P On H.item_code = P.product_code
                        ) As tblTemp
                        Group by Item_Code
                    ''')
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
        unit = request.POST.get('unit',False)
        print(unit)
        type = request.POST.get('type',False)
        size = request.POST.get('size',False)
        return JsonResponse({"product_name":product_name,"type":type,"size":size,"product_desc": product_desc,'unit':unit,'opening_stock':opening_stock})
    if request.method == 'POST':
        items = json.loads(request.POST.get('items'))
        for value in items:
            type = value["type"][:3]
            size = value["size"][:3]
            item_code = type+"-"+size+"-"+str(serial_no)

            new_products = Add_products(product_code = item_code, product_name = value["item_name"], product_desc = value["item_desc"],unit = value["unit"], size = value["size"], type = value["type"] ,opening_stock = value["opening_stock"])
            new_products.save()
            serial_no = serial_no + 1
        return JsonResponse({"result":"success"})
    return render(request, 'inventory/add_product.html')


def edit_item(request,pk):
    all_detail = Add_products.objects.filter(id = pk).first()
    if request.method == "POST":
        type = request.POST.get('type')
        size = request.POST.get('size')
        product_name = request.POST.get('product_name')
        product_desc = request.POST.get('product_desc')
        select_unit = request.POST.get('select_unit')
        opening_stock = request.POST.get('opening_stock')

        all_detail.type = type
        all_detail.size = size
        all_detail.product_name = product_name
        all_detail.product_desc = product_desc
        all_detail.select_unit = select_unit
        all_detail.opening_stock = opening_stock
        all_detail.save()
        return JsonResponse({"result":"success"})
    return render(request, 'inventory/edit_item.html', {'all_detail':all_detail,'pk':pk})
