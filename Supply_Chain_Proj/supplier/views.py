from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import (RfqSupplierHeader,RfqSupplierDetail,
                    QuotationHeaderSupplier, QuotationDetailSupplier,
                    PoHeaderSupplier, PoDetailSupplier,
                    DcHeaderSupplier, DcDetailSupplier,
                    Company_info)
from customer.models import (DcHeaderCustomer, PoHeaderCustomer, QuotationHeaderCustomer, RfqCustomerHeader)
from inventory.models import Add_products
from transaction.models import ChartOfAccount,PurchaseDetail
from django.core import serializers
from django.forms.models import model_to_dict
import json
import datetime
from django.db import IntegrityError
from django.conf import settings
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template
from django.db import connection
from django.db.models import Q
import xlwt
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from user.models import UserRoles
from django.contrib import messages

def customer_roles(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 1)
    form_name = Q(form_name = "Customer")
    allow_quotation_roles = UserRoles.objects.filter(user_id,form_id, form_name).all()
    return allow_quotation_roles


def supplier_roles(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    form_name = Q(form_name = "Supplier")
    allow_po_roles = UserRoles.objects.filter(user_id, form_id, form_name).all()
    return allow_po_roles

def transaction_roles(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    form_name = Q(form_name = "Transaction")
    allow_po_roles = UserRoles.objects.filter(user_id, form_id, form_name).all()
    return allow_po_roles

def inventory_roles(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 4)
    form_name = Q(form_name = "Inventory")
    allow_po_roles = UserRoles.objects.filter(user_id, form_id, form_name).all()
    return allow_po_roles

def report_roles(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 5)
    form_name = Q(form_name = "Reports")
    allow_quotation_roles = UserRoles.objects.filter(user_id,form_id, form_name).all()
    return allow_quotation_roles


def allow_rfq_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 21)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_rfq_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 21)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_rfq_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 21)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_rfq_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 21)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False

def allow_quotation_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 22)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_quotation_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 22)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_quotation_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 22)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_quotation_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 22)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False


def allow_quotation_print(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 22)
    r_print = Q(r_print = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_print)
    if allow_role:
        return True
    else:
        return False



def allow_purchase_order_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 23)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_purchase_order_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 23)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_purchase_order_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 23)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_purchase_order_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 23)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False

def allow_purchase_order_print(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 23)
    r_print = Q(r_print = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_print)
    if allow_role:
        return True
    else:
        return False


def allow_delivery_challan_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 24)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_delivery_challan_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 24)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_delivery_challan_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 24)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_delivery_challan_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 24)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False

def allow_delivery_challan_print(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 24)
    r_print = Q(r_print = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_print)
    if allow_role:
        return True
    else:
        return False


def allow_mrn_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 25)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_mrn_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 2)
    child_form = Q(child_form = 25)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False


def rfq_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 21)
    rfq_roles = UserRoles.objects.filter(user_id,child_form).first()
    return rfq_roles


def quotation_roles2(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 22)
    quotation_roles = UserRoles.objects.filter(user_id,child_form).first()
    return quotation_roles


def purchase_order_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 23)
    po_roles = UserRoles.objects.filter(user_id,child_form).first()
    return po_roles

def delivery_challan_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 24)
    dc_roles = UserRoles.objects.filter(user_id,child_form).first()
    return dc_roles

def mrn_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 25)
    mrn_roles = UserRoles.objects.filter(user_id,child_form).first()
    return mrn_roles


def home(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    print(allow_customer_roles)
    today = datetime.date.today()
    cursor = connection.cursor()
    cursor.execute('''select rfq_no , date, account_id_id
                    from customer_rfqcustomerheader
                    where customer_rfqcustomerheader.show_notification = 1 and customer_rfqcustomerheader.follow_up = %s
                    union
                    select quotation_no, date, account_id_id
                    from customer_quotationheadercustomer
                    where customer_quotationheadercustomer.show_notification = 1 and customer_quotationheadercustomer.follow_up = %s
                    union
                    select po_no, date, account_id_id
                    from customer_poheadercustomer
                    where customer_poheadercustomer.show_notification = 1 and customer_poheadercustomer.follow_up = %s
                    union
                    select dc_no, date, account_id_id
                    from customer_dcheadercustomer
                    where customer_dcheadercustomer.show_notification = 1 and customer_dcheadercustomer.follow_up = %s
                    ''',[today,today,today,today])
    customer_row = cursor.fetchall()
    total_notification = len(customer_row)

    supplier_row = cursor.execute('''select rfq_no , date, account_id_id
                                from supplier_rfqsupplierheader
                                where supplier_rfqsupplierheader.show_notification = 1 and supplier_rfqsupplierheader.follow_up = %s
                                union
                                select quotation_no, date, account_id_id
                                from supplier_quotationheadersupplier
                                where supplier_quotationheadersupplier.show_notification = 1 and supplier_quotationheadersupplier.follow_up = %s
                                union
                                select po_no, date, account_id_id
                                from supplier_poheadersupplier
                                where supplier_poheadersupplier.show_notification = 1 and supplier_poheadersupplier.follow_up = %s
                                union
                                select dc_no, date, account_id_id
                                from supplier_dcheadersupplier
                                where supplier_dcheadersupplier.show_notification = 1 and supplier_dcheadersupplier.follow_up = %s
                                ''',[today,today,today,today])
    supplier_row = supplier_row.fetchall()
    total_notification_supplier = len(supplier_row)
    return render(request,'supplier/base.html',{'total_notification':total_notification,'total_notification_supplier':total_notification_supplier ,'customer_row':customer_row, 'supplier_row':supplier_row, 'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,
    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_rfq_display)
def rfq_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = rfq_roles(request.user)
    all_rfq = RfqSupplierHeader.objects.all()
    return render(request, 'supplier/rfq_supplier.html',{'all_rfq':all_rfq, 'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_rfq_add)
def new_rfq_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    get_last_rfq_no = RfqSupplierHeader.objects.last()
    all_item_code = Add_products.objects.all()
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
        footer_remarks = request.POST.get('footer_remarks',False)
        items = json.loads(request.POST.get('items'))
        try:
            account_id = ChartOfAccount.objects.get(account_title = supplier)
        except ChartOfAccount.DoesNotExist:
            return JsonResponse({"result":"No Account Found "+supplier+""})
        if follow_up:
            follow_up = follow_up
        else:
            follow_up = '2010-10-06'
        date = datetime.date.today()
        rfq_header = RfqSupplierHeader(rfq_no = get_last_rfq_no, date = date , attn = attn, follow_up = follow_up, footer_remarks = footer_remarks ,account_id = account_id, company_id = company, user_id = request.user)
        rfq_header.save()
        header_id = RfqSupplierHeader.objects.get(rfq_no=get_last_rfq_no)
        for value in items:
            id = value["id"]
            id = Add_products.objects.get(id = id)
            rfq_detail = RfqSupplierDetail(item_id = id, quantity = value["quantity"], unit = value["unit"], rfq_id = header_id)
            rfq_detail.save()
        return JsonResponse({"result": "success"})
    return render(request,'supplier/new_rfq_supplier.html',{'get_last_rfq_no':get_last_rfq_no, 'all_item_code':all_item_code, 'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_rfq_edit)
def edit_rfq_supplier(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    rfq_header = RfqSupplierHeader.objects.filter(company,id = pk).first()
    rfq_detail = RfqSupplierDetail.objects.filter(rfq_id = rfq_header.id).all()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    try:
        item_code = request.POST.get('item_code',False)
        if item_code:
            item_id = Add_products.objects.get(product_code = item_code)
            item_code_exist = RfqSupplierDetail.objects.filter(item_id = item_id, rfq_id = rfq_header.id).first()
            data = Add_products.objects.filter(id = item_id.id)
            if item_code_exist:
                return HttpResponse(json.dumps({'message':"Item Already Exist"}))
            row = serializers.serialize('json',data)
            return HttpResponse(json.dumps({'row':row}))
        if request.method == 'POST':
            rfq_detail.delete()
            edit_rfq_supplier_name = request.POST.get('edit_rfq_supplier_name',False)
            edit_rfq_attn = request.POST.get('edit_rfq_attn',False)
            edit_rfq_follow_up = request.POST.get('edit_rfq_follow_up',False)
            edit_footer_remarks = request.POST.get('edit_footer_remarks',False)
            try:
                account_id = ChartOfAccount.objects.get(account_title = edit_rfq_supplier_name)
            except ChartOfAccount.DoesNotExist:
                return JsonResponse({"result":"No Account Found "+edit_rfq_supplier_name+""})
            if edit_rfq_follow_up:
                edit_rfq_follow_up = edit_rfq_follow_up
            else:
                edit_rfq_follow_up = '2010-10-06'
            rfq_header.attn = edit_rfq_attn
            rfq_header.follow_up = edit_rfq_follow_up
            rfq_header.account_id = account_id
            rfq_header.footer_remarks = edit_footer_remarks
            rfq_header.save()
            header_id = RfqSupplierHeader.objects.get(id = pk)
            items = json.loads(request.POST.get('items'))
            for value in items:
                id = value["id"]
                id = Add_products.objects.get(id = id)
                rfq_detail = RfqSupplierDetail(item_id = id, quantity = value["quantity"], unit = value["unit"], rfq_id = header_id, company_id = company, user_id = request.user)
                rfq_detail.save()
            return JsonResponse({"result":"success"})
    except IntegrityError:
        print("Data Already Exist")
    return render(request,'supplier/edit_rfq_supplier.html',{'rfq_header':rfq_header,'pk':pk,'rfq_detail':rfq_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_rfq_delete)
def delete_rfq_supplier(request,pk):
    RfqSupplierDetail.objects.filter(rfq_id_id = pk).all().delete()
    RfqSupplierHeader.objects.filter(id = pk).delete()
    messages.add_message(request, messages.SUCCESS, "Supplier RFQ Deleted")
    return redirect('rfq-supplier')


@user_passes_test(allow_quotation_display)
def quotation_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = quotation_roles2(request.user)
    all_quotation = QuotationHeaderSupplier.objects.all()
    return render(request, 'supplier/quotation_supplier.html',{'all_quotation':all_quotation,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_quotation_add)
def new_quotation_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    get_last_quotation_no = QuotationHeaderSupplier.objects.last()
    all_item_code = Add_products.objects.all()
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
        row = serializers.serialize('json',data)
        print(row)
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
        footer_remarks = request.POST.get('footer_remarks',False)
        if follow_up:
            follow_up = follow_up
        else:
            follow_up = '2010-10-06'
        try:
            account_id = ChartOfAccount.objects.get(account_title = supplier)
        except ChartOfAccount.DoesNotExist:
            return JsonResponse({"result":"No Account Found "+supplier+""})
        date = datetime.date.today()
        quotation_header = QuotationHeaderSupplier(quotation_no = get_last_quotation_no, date = date, attn = attn, prc_basis = prcbasis,
                                                leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
                                                exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True, footer_remarks = footer_remarks, account_id = account_id, company_id = company, user_id = request.user)
        quotation_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = QuotationHeaderSupplier.objects.get(quotation_no = get_last_quotation_no)
        for value in items:
            id = value["id"]
            id = Add_products.objects.get(id = id)
            quotation_detail = QuotationDetailSupplier(item_id = id,  quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_id = header_id)
            quotation_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'supplier/new_quotation_supplier.html',{'all_item_code':all_item_code,'get_last_quotation_no':get_last_quotation_no,'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_quotation_edit)
def edit_quotation_supplier(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    quotation_header = QuotationHeaderSupplier.objects.filter(company, id = pk).first()
    quotation_detail = QuotationDetailSupplier.objects.filter(quotation_id = quotation_header.id).all()
    all_accounts = ChartOfAccount.objects.all()
    print(quotation_detail)
    all_item_code = list(Add_products.objects.values('product_code'))
    item_code = request.POST.get('item_code',False)
    if item_code:
        item_id = Add_products.objects.get(product_code = item_code)
        item_code_exist = QuotationDetailSupplier.objects.filter(item_id = item_id, quotation_id = quotation_header.id).first()
        data = Add_products.objects.filter(id = item_id.id)
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
        edit_footer_remarks = request.POST.get('edit_footer_remarks',False)
        try:
            account_id = ChartOfAccount.objects.get(account_title = edit_supplier)
        except ChartOfAccount.DoesNotExist:
            return JsonResponse({"result":"No Account Found "+edit_supplier+""})

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
        quotation_header.footer_remarks = edit_footer_remarks
        quotation_header.save()

        header_id = QuotationHeaderSupplier.objects.get(id = pk)
        items = json.loads(request.POST.get('items'))
        print(items)
        for value in items:
            id = value["id"]
            id = Add_products.objects.get(id = id)
            quotation_detail = QuotationDetailSupplier(item_id = id,  quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_id = header_id)
            quotation_detail.save()
        return JsonResponse({"result":"success"})
    return render(request,'supplier/edit_quotation_supplier.html',{'quotation_header':quotation_header,'pk':pk,'quotation_detail':quotation_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_quotation_print)
def print_quotation_supplier(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    lines = 0
    total_amount = 0
    company_info = Company_info.objects.all()
    image = Company_info.objects.filter(company_name = "Hamza Enterprise").first()
    header = QuotationHeaderSupplier.objects.filter(company,id = pk).first()
    detail = QuotationDetailSupplier.objects.filter(quotation_id = header.id).all()
    for value in detail:
        lines = lines + len(value.item_description.split('\n'))
        amount = float(value.unit_price * value.quantity)
        total_amount = total_amount + amount
    print(total_amount)
    lines = lines + len(detail) + len(detail)
    total_lines = 36 - lines
    pdf = render_to_pdf('supplier/quotation_supplier_pdf.html', {'company_info':company_info,'image':image,'header':header, 'detail':detail,'total_lines':total_lines,'total_amount':total_amount,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Quotation_Supplier_%s.pdf" %("123")
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@user_passes_test(allow_quotation_delete)
def delete_quotation_supplier(request,pk):
    QuotationDetailSupplier.objects.filter(quotation_id_id = pk).all().delete()
    QuotationHeaderSupplier.objects.filter(id = pk).delete()
    messages.add_message(request, messages.SUCCESS, "Supplier Quotation Deleted")
    return redirect('quotation-supplier')


def quotation_export_supplier(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="QuotationSupplier.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Quotation No', 'Date','Attn' ,'Prc Basis', 'Lead Time', 'Validity', 'Payment', 'Remarks', 'Curreny', 'Exchange Rate', 'Follow Up', 'Footer Remarks']


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = QuotationHeaderSupplier.objects.all().values_list('quotation_no', 'date', 'attn', 'prc_basis', 'leadtime', 'validity', 'payment', 'remarks', 'currency', 'exchange_rate', 'follow_up', 'footer_remarks')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@user_passes_test(allow_purchase_order_display)
def purchase_order_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = purchase_order_roles(request.user)
    all_po = PoHeaderSupplier.objects.all()
    return render(request, 'supplier/purchase_order_supplier.html',{'all_po':all_po,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_purchase_order_add)
def new_purchase_order_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    get_last_po_no = PoHeaderSupplier.objects.last()
    all_item_code = Add_products.objects.all
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
        footer_remarks = request.POST.get('footer_remarks',False)
        try:
            account_id = ChartOfAccount.objects.get(account_title = supplier)
        except ChartOfAccount.DoesNotExist:
            return JsonResponse({"result":"No Account Found "+supplier+""})
        date = datetime.date.today()
        po_header = PoHeaderSupplier(po_no = get_last_po_no, date = date, attn = attn, prc_basis = prcbasis,
                                                leadtime = leadtime, validity = validity, payment = payment, remarks = remarks, currency = currency,
                                                exchange_rate = exchange_rate, follow_up = follow_up, show_notification = True, footer_remarks = footer_remarks ,account_id = account_id, company_id = company, user_id = request.user)
        po_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = PoHeaderSupplier.objects.get(po_no = get_last_po_no)
        for value in items:
            id = value["id"]
            id = Add_products.objects.get(id = id)
            po_detail = PoDetailSupplier(item_id = id, quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_no = "to be define" ,po_id = header_id)
            po_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'supplier/new_purchase_order_supplier.html',{'all_item_code':all_item_code,'get_last_po_no':get_last_po_no, 'all_accounts': all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_purchase_order_edit)
def edit_purchase_order_supplier(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    po_header = PoHeaderSupplier.objects.filter(company, id = pk).first()
    po_detail = PoDetailSupplier.objects.filter(po_id = po_header.id).all()
    all_item_code = list(Add_products.objects.values('product_code'))
    all_accounts = ChartOfAccount.objects.all()
    item_code = request.POST.get('item_code')
    if item_code:
        item_id = Add_products.objects.get(product_code = item_code)
        item_code_exist = PoDetailSupplier.objects.filter(item_id = item_id, po_id = po_header.id).first()
        data = Add_products.objects.filter(id = item_id.id)
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
        edit_footer_remarks = request.POST.get('edit_footer_remarks',False)

        try:
            account_id = ChartOfAccount.objects.get(account_title = edit_po_supplier)
        except ChartOfAccount.DoesNotExist:
            return JsonResponse({"result":"No Account Found "+edit_po_supplier+""})

        po_header.attn = edit_po_attn
        po_header.prc_basis = edit_po_prcbasis
        po_header.leadtime = edit_po_leadtime
        po_header.validity = edit_po_validity
        po_header.payment = edit_po_payment
        po_header.remarks = edit_po_remarks
        po_header.currency = edit_po_currency_rate
        po_header.exchange_rate = edit_po_exchange_rate
        po_header.footer_remarks = edit_footer_remarks
        po_header.follow_up = edit_po_follow_up
        po_header.account_id = account_id
        po_header.save()

        header_id = PoHeaderSupplier.objects.get(id = pk)
        items = json.loads(request.POST.get('items'))
        for value in items:
            id = value["id"]
            id = Add_products.objects.get(id = id)
            po_detail = PoDetailSupplier(item_id = id, quantity = value["quantity"], unit = value["unit"], unit_price = value["unit_price"], remarks = value["remarks"], quotation_no = "to be define" ,po_id = header_id)
            po_detail.save()
        return JsonResponse({"result":"success"})
    return render(request,'supplier/edit_purchase_order_supplier.html',{'po_header':po_header,'pk':pk,'po_detail':po_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_purchase_order_print)
def print_po_supplier(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    lines = 0
    total_amount = 0
    company_info = Company_info.objects.all()
    image = Company_info.objects.filter(id = 1).first()
    print(image.company_logo)
    header = PoHeaderSupplier.objects.filter(company, id = pk).first()
    detail = PoDetailSupplier.objects.filter(po_id = header.id).all()
    for value in detail:
        lines = lines + len(value.item_description.split('\n'))
        amount = float(value.unit_price * value.quantity)
        total_amount = total_amount + amount
    print(total_amount)
    lines = lines + len(detail) + len(detail)
    total_lines = 40 - lines
    pdf = render_to_pdf('supplier/po_supplier_pdf.html', {'company_info':company_info,'image':image,'header':header, 'detail':detail,'total_lines':total_lines,'total_amount':total_amount,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Po_Supplier_%s.pdf" %(header.po_no)
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@user_passes_test(allow_purchase_order_delete)
def delete_purchase_order_supplier(request,pk):
    PoDetailSupplier.objects.filter(po_id_id = pk).all().delete()
    PoHeaderSupplier.objects.filter(id = pk).delete()
    messages.add_message(request, messages.SUCCESS, "Supplier Purchase Order Deleted")
    return redirect('purchase-order-supplier')


@user_passes_test(allow_delivery_challan_display)
def delivery_challan_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = delivery_challan_roles(request.user)
    all_dc = DcHeaderSupplier.objects.all()
    return render(request, 'supplier/delivery_challan_supplier.html',{'all_dc':all_dc,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_delivery_challan_add)
def new_delivery_challan_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    all_item_code = Add_products.objects.all()
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
        item_code_dc = item_code_dc[:12]
        data = Add_products.objects.filter(product_code = item_code_dc)
        for value in data:
            print(value.product_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        dc_supplier = request.POST.get('supplier')
        footer_remarks = request.POST.get('footer_remarks')
        follow_up = request.POST.get('follow_up')
        try:
            account_id = ChartOfAccount.objects.get(account_title = dc_supplier)
        except ChartOfAccount.DoesNotExist:
            return JsonResponse({"result":"No Account Found "+dc_supplier+""})
        date = datetime.date.today()
        dc_header = DcHeaderSupplier(dc_no = get_last_dc_no, date = date, footer_remarks = footer_remarks, follow_up = follow_up ,account_id = account_id, company_id = company, user_id = request.user)
        dc_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = DcHeaderSupplier.objects.get(dc_no = get_last_dc_no)
        for value in items:
            item_id = Add_products.objects.get(id = value["id"])
            dc_detail = DcDetailSupplier(item_id = item_id, quantity = value["quantity"],accepted_quantity = 0, returned_quantity = 0, po_no = "" ,dc_id = header_id)
            dc_detail.save()
        return JsonResponse({'result':'success'})
    return render(request, 'supplier/new_delivery_challan_supplier.html',{'all_item_code':all_item_code,'get_last_dc_no':get_last_dc_no,'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_delivery_challan_edit)
def edit_delivery_challan_supplier(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    dc_header = DcHeaderSupplier.objects.filter(company, id = pk).first()
    dc_detail = DcDetailSupplier.objects.filter(dc_id = dc_header.id).all()
    all_accounts = ChartOfAccount.objects.all()
    all_item_code = list(Add_products.objects.values('product_code'))
    item_code = request.POST.get('item_code')
    if item_code:
        item_id = Add_products.objects.get(product_code = item_code)
        item_code_exist = DcDetailSupplier.objects.filter(item_id = item_id, dc_id = dc_detail.id).first()
        data = Add_products.objects.filter(id = item_id.id)
        if item_code_exist:
            return HttpResponse(json.dumps({'message':"Item Already Exist"}))
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        dc_detail.delete()
        dc_supplier = request.POST.get('supplier')
        follow_up = request.POST.get('follow_up')
        edit_footer_remarks = request.POST.get('edit_footer_remarks')
        try:
            account_id = ChartOfAccount.objects.get(account_title = dc_supplier)
        except ChartOfAccount.DoesNotExist:
            return JsonResponse({"result":"No Account Found "+dc_supplier+""})
        dc_header.account_id = account_id
        dc_header.follow_up = follow_up
        dc_header.footer_remarks = edit_footer_remarks
        dc_header.save()
        header_id = DcHeaderSupplier.objects.get(id = pk)
        items = json.loads(request.POST.get('items'))
        for value in items:
            print(value["id"])
            item_id = Add_products.objects.get(id = value["id"])
            dc_detail = DcDetailSupplier(item_id = item_id, quantity = value["quantity"],accepted_quantity = 0, returned_quantity = 0, po_no = "" ,dc_id = header_id, remarks = value["remarks"], unit = value["unit"])
            dc_detail.save()
        return JsonResponse({"result":"success"})
    return render(request,'supplier/edit_delivery_challan_supplier.html',{'dc_header':dc_header,'pk':pk,'dc_detail':dc_detail, 'all_item_code':all_item_code, 'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_delivery_challan_print)
def print_dc_supplier(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    lines = 0
    company_info = Company_info.objects.all()
    image = Company_info.objects.filter(company_name = "Hamza Enterprise").first()
    header = DcHeaderSupplier.objects.filter(company, id = pk).first()
    detail = DcDetailSupplier.objects.filter(dc_id = header.id).all()
    for value in detail:
        lines = lines + len(value.item_description.split('\n'))
    lines = lines + len(detail) + len(detail)
    total_lines = 40 - lines
    pdf = render_to_pdf('supplier/dc_supplier_pdf.html', {'company_info':company_info,'image':image,'header':header, 'detail':detail,'total_lines':total_lines,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Po_Supplier_%s.pdf" %(header.dc_no)
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@user_passes_test(allow_delivery_challan_delete)
def delete_delivery_challan_supplier(request,pk):
    if PurchaseDetail.objects.filter(dc_ref = pk).all():
        messages.add_message(request, messages.ERROR, "Permission to delete denied.")
    else:
        DcDetailSupplier.objects.filter(dc_id_id = pk).all().delete()
        DcHeaderSupplier.objects.filter(id = pk).delete()
        messages.add_message(request, messages.SUCCESS, "Supplier Delivery Challan Deleted")

    return redirect('delivery-challan-supplier')


@user_passes_test(allow_mrn_display)
def mrn_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = mrn_roles(request.user)
    all_dc = DcHeaderSupplier.objects.all()
    return render(request, 'supplier/mrn_supplier.html',{'all_dc':all_dc,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@user_passes_test(allow_mrn_edit)
def edit_mrn_supplier(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    dc_header = DcHeaderSupplier.objects.filter(company, id=pk).first()
    dc_detail = DcDetailSupplier.objects.filter(dc_id=dc_header.id).all()
    if request.method == 'POST':
        follow_up = request.POST.get('follow_up', False)
        dc_header.follow_up = follow_up
        dc_header.save()
        items = json.loads(request.POST.get('items'))
        for i,value in enumerate(dc_detail):
            value.accepted_quantity = items[i]["accepted_quantity"]
            value.save()
        return JsonResponse({"result":"success"})
    return render(request, 'supplier/edit_mrn_supplier.html',{'dc_header':dc_header,'dc_detail':dc_detail,'pk':pk,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


def show_notification(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    eventId = request.POST.get('eventId', False)
    if eventId:
        if eventId[:2] == "DC":
            account_info = DcHeaderCustomer.objects.filter(company, dc_no = eventId).first()
            tran_no = account_info.dc_no
            account_title = account_info.account_id.account_title
            return JsonResponse({'account_title':account_title, 'tran_no': tran_no})
        elif eventId[:2] == "PO":
            account_info = PoHeaderCustomer.objects.filter(company, po_no = eventId).first()
            tran_no = account_info.po_no
            account_title = account_info.account_id.account_title
            return JsonResponse({'account_title':account_title, 'tran_no': tran_no})
        elif eventId[:2] == "QU":
            account_info = QuotationHeaderCustomer.objects.filter(company, quotation_no = eventId).first()
            tran_no = account_info.quotation_no
            account_title = account_info.account_id.account_title
            return JsonResponse({'account_title':account_title, 'tran_no': tran_no})
        elif eventId[:2] == "RF":
            account_info = RfqCustomerHeader.objects.filter(company, rfq_no = eventId).first()
            tran_no = account_info.rfq_no
            account_title = account_info.account_id.account_title
            return JsonResponse({'account_title':account_title, 'tran_no': tran_no})
    return render(request, 'supplier/index.html',{'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


def update_notification_customer(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    if request.method == "POST":
        postpone_customer = request.POST.get("postpone_customer",False)
        turn_off = request.POST.get("turn_off",False)
        if turn_off:
            turn_off = turn_off
        else:
            turn_off = 1
        if postpone_customer:
            postpone_customer = postpone_customer
        else:
            postpone_customer = datetime.date.today()
        print(postpone_customer)
        tran_no = request.POST.get("tran_no", False)
        if tran_no[:2] == "DC":
            update_dc = DcHeaderCustomer.objects.filter(company, dc_no = tran_no).first()
            update_dc.follow_up = postpone_customer
            update_dc.show_notification = turn_off
            update_dc.save()
            return redirect('home')
        elif tran_no[:2] == "PO":
            update_po = PoHeaderCustomer.objects.filter(company, po_no = tran_no).first()
            update_po.follow_up = postpone_customer
            update_po.show_notification = turn_off
            update_po.save()
            return redirect('home')
        elif tran_no[:2] == "QU":
            update_qu = QuotationHeaderCustomer.objects.filter(company, quotation_no = tran_no).first()
            update_qu.follow_up = postpone_customer
            update_qu.show_notification = turn_off
            update_qu.save()
            return redirect('home')
        elif tran_no[:2] == "RF":
            update_rfq = RfqCustomerHeader.objects.filter(company, rfq_no = tran_no).first()
            update_rfq.follow_up = postpone_customer
            update_rfq.show_notification = turn_off
            update_rfq.save()
            return redirect('home')
    return redirect('home')


def show_notification_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    eventId = request.POST.get('eventId', False)
    if eventId:
        if eventId[:2] == "DC":
            account_info = DcHeaderSupplier.objects.filter(company, dc_no = eventId).first()
            tran_no = account_info.dc_no
            account_title = account_info.account_id.account_title
            return JsonResponse({'account_title':account_title, 'tran_no': tran_no})
        elif eventId[:2] == "PO":
            account_info = PoHeaderSupplier.objects.filter(company, po_no = eventId).first()
            tran_no = account_info.po_no
            account_title = account_info.account_id.account_title
            return JsonResponse({'account_title':account_title, 'tran_no': tran_no})
        elif eventId[:2] == "QU":
            account_info = QuotationHeaderSupplier.objects.filter(company, quotation_no = eventId).first()
            tran_no = account_info.quotation_no
            account_title = account_info.account_id.account_title
            return JsonResponse({'account_title':account_title, 'tran_no': tran_no})
        elif eventId[:2] == "RF":
            account_info = RfqSupplierHeader.objects.filter(company, rfq_no = eventId).first()
            tran_no = account_info.rfq_no
            account_title = account_info.account_id.account_title
            return JsonResponse({'account_title':account_title, 'tran_no': tran_no})
    return render(request, 'supplier/index.html',{'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


def update_notification_supplier(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    if request.method == "POST":
        postpone_supplier = request.POST.get("postpone_supplier",False)
        turn_off = request.POST.get("turn_off",False)
        if turn_off:
            turn_off = turn_off
        else:
            turn_off = 1
        if postpone_supplier:
            postpone_supplier = postpone_supplier
        else:
            postpone_supplier = datetime.date.today()
        print(postpone_supplier)
        tran_no = request.POST.get("tran_no", False)
        print(tran_no)
        if tran_no[:2] == "DC":
            update_dc = DcHeaderSupplier.objects.filter(company, dc_no = tran_no).first()
            update_dc.follow_up = postpone_supplier
            update_dc.show_notification = turn_off
            update_dc.save()
            return redirect('home')
        elif tran_no[:2] == "PO":
            update_po = PoHeaderSupplier.objects.filter(company, po_no = tran_no).first()
            update_po.follow_up = postpone_supplier
            update_po.show_notification = turn_off
            update_po.save()
            return redirect('home')
        elif tran_no[:2] == "QU":
            update_qu = QuotationHeaderSupplier.objects.filter(company, quotation_no = tran_no).first()
            update_qu.follow_up = postpone_supplier
            update_qu.show_notification = turn_off
            update_qu.save()
            return redirect('home')
        elif tran_no[:2] == "RF":
            update_rfq = RfqSupplierHeader.objects.filter(company, rfq_no = tran_no).first()
            update_rfq.follow_up = postpone_supplier
            update_rfq.show_notification = turn_off
            update_rfq.save()
            return redirect('home')
    return redirect('home')


def journal_voucher(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    account_title = request.POST.get('account_title', False)
    print(account_title)
    return render('transaction/journal_voucher.html',{'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})
