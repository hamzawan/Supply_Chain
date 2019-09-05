from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import (Add_products, Category, SubCategory)
from transaction.models import (PurchaseDetail, SaleDetail)
from itertools import chain
import json
from django.db import connection
from django.contrib import messages
from supplier.views import customer_roles,supplier_roles,transaction_roles,inventory_roles,report_roles
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
from user.models import UserRoles
from django.core import serializers


def inventory_form_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 41)
    inventory_roles = UserRoles.objects.filter(user_id,child_form).first()
    return inventory_roles

def allow_inventory_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 4)
    child_form = Q(child_form = 41)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_inventory_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 4)
    child_form = Q(child_form = 41)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_inventory_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 4)
    child_form = Q(child_form = 41)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_inventory_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 4)
    child_form = Q(child_form = 41)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False

def allow_inventory_shop(user):
    user_id = Q(user_id = 2)
    form_id = Q(form_id = 4)
    child_form = Q(child_form = 41)
    r_print = Q(r_print = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_print)
    print(allow_role)
    if allow_role:
        return True
    else:
        return False


@login_required
@user_passes_test(allow_inventory_display)
def item_stock(request):
    permission = inventory_form_roles(request.user)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    cursor = connection.cursor()
    cursor.execute('''Select itemID,Size,item_code, item_name,Item_description,Unit,Size,SUM(quantity) As qty, main_category, sub_category From (
                    Select 'Opening Stock' As TranType,ID As ItemID, Size,Product_Code As Item_Code,Product_Name As Item_name,Product_desc As Item_description,Unit As unit,Opening_Stock as Quantity, main_category, sub_category
                    From inventory_add_products
                    union all
                    Select 'Purchase' As TranType,P.ID As ItemID,P.Size,P.Product_Code,P.Product_name,P.Product_desc,P.unit,Quantity,P.main_category, P.sub_category
                    From transaction_purchasedetail H Inner join inventory_add_products P On H.item_id_id = P.id
                    union All
                    Select 'Purchase Return' As TranType,P.ID As ItemID,P.Size,P.Product_Code,P.Product_name,P.Product_desc,P.unit,Quantity * -1,P.main_category, P.sub_category
                    From transaction_purchasereturndetail H Inner join inventory_add_products P On H.item_id_id = P.id
                    union all
                    Select 'Sale' As TranType,P.ID AS ItemID,P.Size,P.Product_Code,P.Product_name,P.Product_desc,P.unit,Quantity * -1,P.main_category, P.sub_category
                    From transaction_saledetail H Inner join inventory_add_products P On H.item_id_id = P.id
                    union all
                    Select 'Sale Return' As TranType,P.ID AS ItemID,P.Size,P.Product_Code,P.Product_name,P.Product_desc,P.unit,Quantity,P.main_category, P.sub_category
                    From transaction_salereturndetail H Inner join inventory_add_products P On H.item_id_id = P.id
                    ) As tblTemp
                    Group by Item_Code
                    ''')
    row = cursor.fetchall()
    return render(request, 'inventory/item_stock.html',{'row':row,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,
    'permission':permission,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_inventory_add)
def new_item_stock(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    return render(request, 'inventory/new_item_stock.html',{'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_inventory_add)
def add_product(request):
    id = request.POST.get('id', False)
    if id:
        sub_categories_list = SubCategory.objects.filter(main_category_id = id).all()
        list = serializers.serialize('json',sub_categories_list)
        print("Hamza")
        return JsonResponse({"list":list})
    serial_no = 0
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    get_item_code = Add_products.objects.last()
    main_categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    if get_item_code:
        get_item_code = get_item_code.product_code
        serial_no = int(get_item_code) + 1
    else:
        serial_no = '1001'
    product_name = request.POST.get('product_name',False)
    product_desc = request.POST.get('product_desc',False)
    type = request.POST.get('type',False)
    size = request.POST.get('size',False)
    if product_name and product_desc and type and size:
        type = request.POST.get('type',False)
        size = request.POST.get('size',False)
        product_name = request.POST.get('product_name',False)
        product_desc = request.POST.get('product_desc',False)
        opening_stock = request.POST.get('opening_stock',False)
        unit = request.POST.get('unit',False)
        main_category_id = Category.objects.filter(main = type).first()
        sub_category_id = SubCategory.objects.filter(sub = size).first()
        return JsonResponse({"product_name":product_name,"type":type,"size":size,"product_desc": product_desc,'unit':unit,'opening_stock':opening_stock,'main_category_id':main_category_id.id, 'sub_category_id':sub_category_id.id})
    if request.method == 'POST':
        items = json.loads(request.POST.get('items'))
        for value in items:
            item_code = str(serial_no)
            main_category_id = Category.objects.get(id = value["main_category_id"])
            sub_category_id = SubCategory.objects.get(id = value["sub_category_id"])
            new_products = Add_products(product_code = item_code, product_name = value["item_name"], product_desc = value["item_description"],unit = value["unit"], size = value["size"], type = "" ,opening_stock = value["opening_stock"], user_id = request.user ,main_category_id = main_category_id, sub_category_id = sub_category_id, main_category = main_category_id.main, sub_category = sub_category_id.sub )
            new_products.save()
            serial_no = int(serial_no) + 1
        return JsonResponse({"result":"success"})
    return render(request, 'inventory/add_product.html',{'main_categories':main_categories,'sub_categories':sub_categories,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_inventory_edit)
def edit_item(request,pk):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    all_detail = Add_products.objects.filter(id = pk).first()
    main_categories = Category.objects.all()
    sub_categories = SubCategory.objects.filter(main_category_id = all_detail.main_category_id)
    if request.method == "POST":
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        size = request.POST.get('size')
        product_desc = request.POST.get('product_desc')
        select_unit = request.POST['unit']
        opening_stock = request.POST.get('opening_stock')
        main = Category.objects.filter(id = main_category).first()
        sub = SubCategory.objects.filter(id = sub_category).first()
        product_name = main.main+" "+sub.sub+" "+size
        all_detail.sub_category_id = sub
        all_detail.sub_category = sub.sub
        all_detail.size = size
        all_detail.product_name = product_name
        all_detail.product_desc = product_desc
        all_detail.unit = select_unit
        all_detail.opening_stock = opening_stock
        all_detail.save()
    return render(request, 'inventory/edit_item.html', {'all_detail':all_detail,'pk':pk,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser,'main_categories':main_categories,'sub_categories':sub_categories})



def item_avaliable(pk):
    cusror = connection.cursor()
    row = cusror.execute('''select case
                             when exists (select id from customer_rfqcustomerdetail  where item_id_id = %s)
                               or exists (select id from customer_quotationdetailcustomer where item_id_id = %s)
                               or exists (select id from customer_podetailcustomer  where item_id_id = %s)
                        	   or exists (select id from customer_dcdetailcustomer  where item_id_id = %s)
                        	   or exists (select id from transaction_saledetail  where item_id_id = %s)
                        	   or exists (select id from transaction_purchasedetail  where item_id_id = %s)
                              then 'y'
                             else 'n'
                             end
                            ''',[pk,pk,pk,pk,pk,pk])
    row = row.fetchall()
    res_list = [x[0] for x in row]
    if res_list[0] == "n":
        Add_products.objects.filter(id = pk).delete()
        return True
    else:
        return False

@login_required
@user_passes_test(allow_inventory_delete)
def delete_item(request, pk):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    item = item_avaliable(pk)
    if item == True:
        messages.add_message(request, messages.SUCCESS, "Item Deleted")
        return redirect('item-stock')
    else:
        messages.add_message(request, messages.ERROR, "You cannot delete this item, it is refrenced")
        return redirect('item-stock')


@login_required
def categories(request):
    permission = inventory_form_roles(request.user)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    main_categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    return render(request,'inventory/category_and_type.html',{'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser, 'main_categories':main_categories,'sub_categories':sub_categories})


@login_required
def main_categories(request):
    last_code = Category.objects.last()
    if last_code:
        last_code = int(last_code.category_code) + 1
    else:
        last_code = 101
    if request.method == "POST":
        main_category_name = request.POST.get('main_category_name')
        add_main_category = Category(category_code = last_code, main = main_category_name)
        add_main_category.save()
    return redirect('categories')


@login_required
def edit_main_categories(request):
    if request.method == "POST":
        main_category_code = request.POST.get('main_category_code')
        main_category_name_edit = request.POST.get('main_category_name_edit')
        main_category_id = Category.objects.get(category_code = main_category_code)
        cat = Category.objects.filter(category_code = main_category_code).first()
        cat.main = main_category_name_edit
        cat.save()
        items = Add_products.objects.filter(main_category_id = main_category_id.id).all()
        for value in items:
            value.main_category = main_category_name_edit
            update_item_name = main_category_name_edit+" "+value.sub_category+" "+value.size
            value.product_name = update_item_name
            value.save()
    return redirect('categories')


@login_required
def sub_categories(request):
    if request.method == "POST":
        main_category_id = request.POST.get('main_category')
        sub_category_name = request.POST.get('sub_category_name')
        main_category_code = Category.objects.filter(id = main_category_id).first()
        last_code = SubCategory.objects.filter(main_category_id = main_category_id).last()
        if last_code:
            last_code = int(last_code.sub_category_code) + 1
        else:
            last_code = int(str(main_category_code.category_code) + str(1))
        add_sub_category = SubCategory(sub_category_code = last_code, sub = sub_category_name, main_category_id = main_category_code)
        add_sub_category.save()
    return redirect('categories')


@login_required
def edit_sub_categories(request):
    if request.method == "POST":
        sub_category_code = request.POST.get('sub_category_id')
        print("sub_category_code",sub_category_code)
        sub_category_name_edit = request.POST.get('sub_category_name_edit')
        main_category = request.POST.get('main_category')
        main_category_id_from = request.POST.get('main_category_id')
        main_category_code = Category.objects.filter(id = main_category).first()
        cat = SubCategory.objects.filter(id = sub_category_code).first()
        last_code = SubCategory.objects.filter(main_category_id = main_category).last()
        if last_code:
            last_code = int(last_code.sub_category_code) + 1
        else:
            last_code = int(str(main_category_code.category_code) + str(1))
        cat.sub = sub_category_name_edit
        cat.main_category_id = main_category_code
        # cat.sub_category_code = last_code
        cat.save()
        items = Add_products.objects.filter(main_category_id = main_category_id_from,sub_category_id = cat.id).all()
        for value in items:
            value.sub_category = sub_category_name_edit
            update_item_name = main_category_code.main+" "+sub_category_name_edit+" "+value.size
            value.product_name = update_item_name
            value.main_category_id = main_category_code
            value.main_category = main_category_code.main
            value.save()
    return redirect('categories')



def main_category_avaliable(pk):
    cusror = connection.cursor()
    row = cusror.execute('''select case
                                when exists (select id from inventory_subcategory  where main_category_id_id = %s)
                                then 'y'
                                else 'n'
                                end''',[pk])
    row = row.fetchall()
    res_list = [x[0] for x in row]
    if res_list[0] == "n":
        Category.objects.filter(id = pk).delete()
        return True
    else:
        return False


@login_required
def delete_categories(request,pk):
    category = main_category_avaliable(pk)
    if category == True:
        messages.add_message(request, messages.SUCCESS, "Main Category Deleted")
        return redirect('categories')
    else:
        messages.add_message(request, messages.ERROR, "You cannot delete this Category, it is refrenced")
    return redirect('categories')



def sub_category_avaliable(pk):
    cusror = connection.cursor()
    row = cusror.execute('''select case
                            when exists (select id from inventory_add_products  where sub_category_id_id = %s)
                            then 'y'
                            else 'n'
                            end
                            ''',[pk])
    row = row.fetchall()
    res_list = [x[0] for x in row]
    if res_list[0] == "n":
        SubCategory.objects.filter(id = pk).delete()
        return True
    else:
        return False


@login_required
def delete_sub_categories(request,pk):
    category = sub_category_avaliable(pk)
    if category == True:
        messages.add_message(request, messages.SUCCESS, "Sub Category Deleted")
        return redirect('categories')
    else:
        messages.add_message(request, messages.ERROR, "You cannot delete this Category, it is refrenced")
    return redirect('categories')
