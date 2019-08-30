from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import (PurchaseHeader, PurchaseDetail, SaleHeader, SaleDetail, ChartOfAccount,
                    PurchaseReturnHeader, PurchaseReturnDetail, SaleReturnHeader, SaleReturnDetail,
                    Transactions, VoucherHeader, VoucherDetail, Cartage_and_Po)
from supplier.models import Company_info
from .forms import CompanyUpdateForm,COAUpdateForm
from inventory.models import Add_products
from customer.models import DcHeaderCustomer, DcDetailCustomer
from django.core import serializers
from django.db.models import Q, Count, Sum
import json, datetime
from decimal import Decimal
from supplier.utils import render_to_pdf
from django.template.loader import get_template
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from user.models import UserRoles
from user.views import Is_superuser
from django.contrib.auth.decorators import user_passes_test, login_required
from supplier.views import customer_roles,supplier_roles,transaction_roles,inventory_roles,report_roles
from django.contrib import messages
from num2words import num2words
from supplier.models import Company_info
from collections import defaultdict



def allow_coa_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 31)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_coa_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 31)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_coa_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 31)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False


def allow_purchase_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 32)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_purchase_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 32)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_purchase_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 32)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_purchase_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 32)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False


def allow_purchase_return(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 32)
    r_return = Q(r_return = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_return)
    if allow_role:
        return True
    else:
        return False



def allow_purchase_return_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 33)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_purchase_return_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 33)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_purchase_return_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 33)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_purchase_return_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 33)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False



def allow_sale_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 34)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_sale_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 34)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_sale_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 34)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_sale_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 34)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False

def allow_sale_return(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 34)
    r_return = Q(r_return = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_return)
    if allow_role:
        return True
    else:
        return False


def allow_sale_return_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 35)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_sale_return_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 35)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False


def allow_sale_return_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 35)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_sale_return_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 35)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False



def allow_jv_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 36)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_jv_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 36)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False


def allow_jv_print(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 36)
    r_print = Q(r_print = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_print)
    if allow_role:
        return True
    else:
        return False

def allow_jv_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 36)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False

def allow_jv_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 36)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False


def allow_brv_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 37)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_brv_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 37)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_brv_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 37)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_brv_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 37)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False


def allow_brv_print(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 37)
    r_print = Q(r_print = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_print)
    if allow_role:
        return True
    else:
        return False



def allow_crv_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 38)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_crv_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 38)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_crv_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 38)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_crv_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 38)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False


def allow_crv_print(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 38)
    r_print = Q(r_print = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_print)
    if allow_role:
        return True
    else:
        return False


def allow_bpv_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 39)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_bpv_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 39)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False

def allow_bpv_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 39)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False

def allow_bpv_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 39)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False


def allow_bpv_print(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 39)
    r_print = Q(r_print = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_print)
    if allow_role:
        return True
    else:
        return False



def allow_cpv_display(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 310)
    display = Q(display = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, display)
    if allow_role:
        return True
    else:
        return False


def allow_cpv_add(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 310)
    add = Q(add = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, add)
    if allow_role:
        return True
    else:
        return False



def allow_cpv_edit(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 310)
    edit = Q(edit = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, edit)
    if allow_role:
        return True
    else:
        return False


def allow_cpv_delete(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 310)
    delete = Q(delete = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, delete)
    if allow_role:
        return True
    else:
        return False

def allow_cpv_print(user):
    user_id = Q(user_id = user.id)
    form_id = Q(form_id = 3)
    child_form = Q(child_form = 310)
    r_print = Q(r_print = 1)
    allow_role = UserRoles.objects.filter(user_id, form_id, child_form, r_print)
    if allow_role:
        return True
    else:
        return False


def chart_account_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 31)
    coa_roles = UserRoles.objects.filter(user_id,child_form).first()
    return coa_roles

def purchase_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 32)
    purchase_roles = UserRoles.objects.filter(user_id,child_form).first()
    return purchase_roles

def purchase_return_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 33)
    purchase_return_roles = UserRoles.objects.filter(user_id,child_form).first()
    return purchase_return_roles

def sale_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 34)
    sale_roles = UserRoles.objects.filter(user_id,child_form).first()
    return sale_roles

def sale_return_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 35)
    sale_return_roles = UserRoles.objects.filter(user_id,child_form).first()
    return sale_return_roles


def journal_voucher_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 36)
    journal_voucher_roles = UserRoles.objects.filter(user_id,child_form).first()
    return journal_voucher_roles

def brv_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 37)
    brv_roles = UserRoles.objects.filter(user_id,child_form).first()
    return brv_roles

def crv_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 38)
    crv_roles = UserRoles.objects.filter(user_id,child_form).first()
    return crv_roles


def bpv_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 39)
    bpv_roles = UserRoles.objects.filter(user_id,child_form).first()
    return bpv_roles


def cpv_roles(user):
    userid = str(user.id)
    user_id = Q(user_id= userid)
    child_form = Q(child_form= 310)
    cpv_roles = UserRoles.objects.filter(user_id,child_form).first()
    return cpv_roles


@login_required
@user_passes_test(allow_purchase_display)
def purchase(request):
    company =  request.session['company']
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = purchase_roles(request.user)
    print("here", company)
    all_purchases = PurchaseHeader.objects.filter(company_id = company).all()
    print("Here", all_purchases)
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    gst = Company_info.objects.filter(id = company.id).first()
    return render(request, 'transaction/purchase.html',{'all_purchases': all_purchases,'gst':gst,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_purchase_add)
def new_purchase(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    amount = 0
    item_amount = 0
    sales_tax = 0
    price = 0
    all_item_code = Add_products.objects.all()
    customer = Q(account_id = "100")
    supplier = Q(account_id = "200")
    all_accounts = ChartOfAccount.objects.filter(customer|supplier).all()
    get_last_purchase_no = PurchaseHeader.objects.filter(company_id = company.id).last()
    if get_last_purchase_no:
        get_last_purchase_no = get_last_purchase_no.purchase_no
        num = int(get_last_purchase_no)
        num = num + 1
        get_last_purchase_no = str(num)
    else:
        get_last_purchase_no = '101'
    item_code = request.POST.get('item_code_purchase',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id',False)
        supplier = request.POST.get('supplier',False)
        credit_days = request.POST.get('credit_days',False)
        follow_up = request.POST.get('follow_up',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        withholding_tax = request.POST.get('withholding_tax',False)
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        date = datetime.date.today()
        if follow_up:
            follow_up = follow_up
        else:
            follow_up = '2010-06-10'
        purchase_header = PurchaseHeader(purchase_no = purchase_id, date = date, footer_description = footer_desc, payment_method = payment_method, cartage_amount = cartage_amount, additional_tax = additional_tax, withholding_tax = withholding_tax, account_id = account_id, follow_up = follow_up, credit_days = credit_days, company_id = company, user_id = request.user)

        items = json.loads(request.POST.get('items'))
        purchase_header.save()
        header_id = PurchaseHeader.objects.filter(company_id = company.id).get(purchase_no = purchase_id)
        for value in items:
            item_id = Add_products.objects.get(id = value["id"])
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
            purchase_detail = PurchaseDetail(item_id = item_id, quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], purchase_id = header_id, total = amount)
            purchase_detail.save()
        item_amount = item_amount + float(cartage_amount) + float(additional_tax)
        tax = ((item_amount * float(withholding_tax)) / 100)
        total_amount = tax + item_amount
        header_id = header_id.id

        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        if payment_method == 'Cash':
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Invoice", amount = total_amount, date = date, remarks = purchase_id,ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran2.save()
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Purchase Invoice", amount = -abs(total_amount), date = date, remarks = purchase_id,ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran1.save()
        else:
            purchase_account = ChartOfAccount.objects.get(account_title = 'Purchases')
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Invoice", amount = -abs(total_amount), date = date, remarks = purchase_id,ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = purchase_account, tran_type = "Purchase Invoice", amount = total_amount, date = date, remarks = purchase_id,ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/new_purchase.html',{'all_item_code':all_item_code,'get_last_purchase_no':get_last_purchase_no, 'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_purchase_edit)
def edit_purchase(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    item_amount = 0
    total_amount = 0
    all_item_code = Add_products.objects.all()
    purchase_header = PurchaseHeader.objects.filter(company, id = pk).first()
    purchase_detail = PurchaseDetail.objects.filter(purchase_id = purchase_header.id).all()
    customer = Q(account_id = "100")
    supplier = Q(account_id = "200")
    all_accounts = ChartOfAccount.objects.filter(customer|supplier).all()
    item_code = request.POST.get('item_code_purchase',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        purchase_detail.delete()

        purchase_id = request.POST.get('purchase_id',False)
        supplier = request.POST.get('supplier',False)
        follow_up = request.POST.get('follow_up',False)
        payment_method = request.POST.get('payment_method',False)
        credit_days = request.POST.get('credit_days',False)
        footer_desc = request.POST.get('footer_desc',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        withholding_tax = request.POST.get('withholding_tax',False)
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        if follow_up:
            follow_up = follow_up
        else:
            follow_up = '2010-06-10'
        date = datetime.date.today()
        purchase_header.credit_days = credit_days
        purchase_header.follow_up = follow_up
        purchase_header.payment_method = payment_method
        purchase_header.footer_description = footer_desc
        purchase_header.cartage_amount = cartage_amount
        purchase_header.additional_tax = additional_tax
        purchase_header.withholding_tax = withholding_tax
        purchase_header.account_id = account_id
        purchase_header.credit_days = credit_days
        purchase_header.save()

        items = json.loads(request.POST.get('items'))
        purchase_header.save()
        header_id = PurchaseHeader.objects.filter(company_id = company.id).get(purchase_no = purchase_id)
        for value in items:
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
            item_id = Add_products.objects.get(id = value["id"])
            purchase_detail = PurchaseDetail(item_id = item_id, quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], purchase_id = header_id, total = amount)
            purchase_detail.save()
        item_amount = item_amount + float(cartage_amount) + float(additional_tax)
        # tax = ((item_amount * float(withholding_tax)) / 100)
        total_amount = item_amount
        header_id = header_id.id
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        company =  request.session['company']
        company = Company_info.objects.get(id = company)
        if purchase_header.payment_method == 'Cash':
            refrence_id = Q(refrence_id = header_id)
            tran_type = Q(tran_type = "Purchase Invoice")
            delete = Transactions.objects.filter(refrence_id, tran_type)
            delete.delete()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Invoice", amount = total_amount, date = date, remarks = purchase_id, ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company , user_id = request.user)
            tran2.save()
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Purchase Invoice", amount = -abs(total_amount), date = date, remarks = purchase_id, ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company , user_id = request.user)
            tran1.save()
        else:
            refrence_id = Q(refrence_id = header_id)
            tran_type = Q(tran_type = "Purchase Invoice")
            delete = Transactions.objects.filter(refrence_id, tran_type)
            delete.delete()
            purchase_account = ChartOfAccount.objects.get(account_title = 'Purchases')
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Invoice", amount = -abs(total_amount), date = date, remarks = purchase_id, ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company , user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = purchase_account, tran_type = "Purchase Invoice", amount = total_amount, date = date, remarks = purchase_id, ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company , user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/edit_purchase.html',{'all_item_code':all_item_code,'all_accounts':all_accounts, 'purchase_header':purchase_header, 'purchase_detail':purchase_detail, 'pk':pk,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_purchase_add)
def new_purchase_non_gst(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    amount = 0
    item_amount = 0
    sales_tax = 0
    price = 0
    all_item_code = Add_products.objects.all()
    customer = Q(account_id = "100")
    supplier = Q(account_id = "200")
    all_accounts = ChartOfAccount.objects.filter(customer|supplier).all()
    get_last_purchase_no = PurchaseHeader.objects.filter(company_id = company.id).last()
    if get_last_purchase_no:
        get_last_purchase_no = get_last_purchase_no.purchase_no
        num = int(get_last_purchase_no)
        num = num + 1
        get_last_purchase_no = str(num)
    else:
        get_last_purchase_no = '101'
    item_code = request.POST.get('item_code_purchase',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id',False)
        supplier = request.POST.get('supplier',False)
        credit_days = request.POST.get('credit_days',False)
        follow_up = request.POST.get('follow_up',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        date = datetime.date.today()
        if follow_up:
            follow_up = follow_up
        else:
            follow_up = '2010-06-10'
        purchase_header = PurchaseHeader(purchase_no = purchase_id, date = date, footer_description = footer_desc, payment_method = payment_method, cartage_amount = 0.00, additional_tax = 0.00, withholding_tax = 0.00, account_id = account_id, follow_up = follow_up, credit_days = credit_days, company_id = company, user_id = request.user)

        items = json.loads(request.POST.get('items'))
        purchase_header.save()
        header_id = PurchaseHeader.objects.filter(company_id = company.id).get(purchase_no = purchase_id)
        for value in items:
            item_id = Add_products.objects.get(id = value["id"])
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
            purchase_detail = PurchaseDetail(item_id = item_id, quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = 0.00, purchase_id = header_id, total = amount)
            purchase_detail.save()
        total_amount = item_amount
        header_id = header_id.id
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        if payment_method == 'Cash':
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Invoice", amount = total_amount, date = date, remarks = purchase_id,ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran2.save()
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Purchase Invoice", amount = -abs(total_amount), date = date, remarks = purchase_id,ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran1.save()
        else:
            purchase_account = ChartOfAccount.objects.get(account_title = 'Purchases')
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Invoice", amount = -abs(total_amount), date = date, remarks = purchase_id,ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = purchase_account, tran_type = "Purchase Invoice", amount = total_amount, date = date, remarks = purchase_id,ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/new_purchase_non_gst.html',{'all_item_code':all_item_code,'get_last_purchase_no':get_last_purchase_no, 'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_purchase_edit)
def edit_purchase_non_gst(request,pk):
    cartage_sum = 0
    amount = 0
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    item_amount = 0
    total_amount = 0
    all_item_code = Add_products.objects.all()
    purchase_header = PurchaseHeader.objects.filter(company, id = pk).first()
    purchase_detail = PurchaseDetail.objects.filter(purchase_id = purchase_header.id).all()
    customer = Q(account_id = "100")
    supplier = Q(account_id = "200")
    all_accounts = ChartOfAccount.objects.filter(customer|supplier).all()
    item_code = request.POST.get('item_code_purchase',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        purchase_detail.delete()

        purchase_id = request.POST.get('purchase_id',False)
        supplier = request.POST.get('supplier',False)
        follow_up = request.POST.get('follow_up',False)
        payment_method = request.POST.get('payment_method',False)
        credit_days = request.POST.get('credit_days',False)
        footer_desc = request.POST.get('footer_desc',False)
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        if follow_up:
            follow_up = follow_up
        else:
            follow_up = '2010-06-10'
        date = datetime.date.today()
        purchase_header.credit_days = credit_days
        purchase_header.follow_up = follow_up
        purchase_header.payment_method = payment_method
        purchase_header.footer_description = footer_desc
        purchase_header.cartage_amount = 0.00
        purchase_header.additional_tax = 0.00
        purchase_header.withholding_tax = 0.00
        purchase_header.account_id = account_id
        purchase_header.credit_days = credit_days
        purchase_header.save()

        items = json.loads(request.POST.get('items'))
        cart = json.loads(request.POST.get('cartage'))
        purchase_header.save()
        company =  request.session['company']
        company = Company_info.objects.get(id = company)
        header_id = PurchaseHeader.objects.filter(company_id = company).get(purchase_no = purchase_id)
        Cartage_and_Po.objects.filter(invoice_id = header_id.id).all().delete()
        for value in cart:
            cartage_ = Cartage_and_Po(cartage = value["cartage_amount"], po_no = value["po_no"], invoice_id = header_id.id)
            cartage_.save()
            cartage_sum = cartage_sum + float(value["cartage_amount"])
        for value in items:
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
            item_id = Add_products.objects.get(id = value["id"])
            purchase_detail = PurchaseDetail(item_id = item_id, quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = 0, purchase_id = header_id, total = amount)
            purchase_detail.save()
        item_amount = item_amount
        total_amount = item_amount + cartage_sum
        header_id = header_id.id
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        company =  request.session['company']
        company = Company_info.objects.get(id = company)
        if purchase_header.payment_method == 'Cash':
            refrence_id = Q(refrence_id = header_id)
            tran_type = Q(tran_type = "Purchase Invoice")
            delete = Transactions.objects.filter(refrence_id, tran_type)
            delete.delete()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Invoice", amount = total_amount, date = date, remarks = "Amount Debit", ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company , user_id = request.user)
            tran2.save()
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Purchase Invoice", amount = -abs(total_amount), date = date, remarks = "Amount Debit", ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company , user_id = request.user)
            tran1.save()
        else:
            refrence_id = Q(refrence_id = header_id)
            tran_type = Q(tran_type = "Purchase Invoice")
            delete = Transactions.objects.filter(refrence_id, tran_type)
            delete.delete()
            purchase_account = ChartOfAccount.objects.get(account_title = 'Purchases')
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Invoice", amount = -abs(total_amount), date = date, remarks = "Amount Debit", ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company , user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = purchase_account, tran_type = "Purchase Invoice", amount = total_amount, date = date, remarks = "Amount Debit", ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company , user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/edit_purchase_non_gst.html',{'all_item_code':all_item_code,'all_accounts':all_accounts, 'purchase_header':purchase_header, 'purchase_detail':purchase_detail, 'pk':pk,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})



def voucher_avaliable_purchase(pk):
    cusror = connection.cursor()
    row = cusror.execute('''select case
                            when exists (select id from transaction_voucherdetail  where  invoice_id = %s)
                            then 'y'
                            else 'n'
                            end''',[pk])
    row = row.fetchall()
    res_list = [x[0] for x in row]
    if res_list[0] == "n":
        refrence_id = Q(refrence_id = pk)
        tran_type = Q(tran_type = "Purchase Invoice")
        ref_inv_tran_id = Q(ref_inv_tran_id = pk)
        ref_inv_tran_type = Q(ref_inv_tran_type = "Purchase CPV")
        Transactions.objects.filter(refrence_id , tran_type).all().delete()
        Transactions.objects.filter(ref_inv_tran_id , ref_inv_tran_type).all().delete()
        PurchaseDetail.objects.filter(purchase_id = pk).all().delete()
        PurchaseHeader.objects.filter(id = pk).delete()
        return True
    else:
        return False


@user_passes_test(allow_purchase_delete)
def delete_purchase(request, pk):
    item = voucher_avaliable_purchase(pk)
    if item == True:
        messages.add_message(request, messages.SUCCESS, "Purchase Invoice Deleted.")
        return redirect('purchase')
    else:
        messages.add_message(request, messages.ERROR, "You cannot delete this Invoice, kindly delet it's voucher first.")
        return redirect('purchase')


@login_required
def purchase_return_summary(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    all_purchase_return = PurchaseReturnHeader.objects.all()
    return render(request, 'transaction/purchase_return_summary.html',{'all_purchase_return': all_purchase_return,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_purchase_return_display)
def new_purchase_return(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = purchase_return_roles(request.user)
    total_amount = 0
    item_amount = 0
    get_last_purchase_no = PurchaseReturnHeader.objects.last()
    if get_last_purchase_no:
        get_last_purchase_no = get_last_purchase_no.purchase_no
        get_last_purchase_no = get_last_purchase_no[-3:]
        num = int(get_last_purchase_no)
        num = num + 1
        get_last_purchase_no = 'PUR/RET/' + str(num)
    else:
        get_last_purchase_no = 'PUR/RET/101'
    purchase_header = PurchaseHeader.objects.filter(company, id = pk).first()
    purchase_detail = PurchaseDetail.objects.filter(purchase_id = purchase_header.id).all()
    if request.method == 'POST':
        company =  request.session['company']
        company = Company_info.objects.get(id = company)
        supplier = request.POST.get('supplier',False)
        credit_days = purchase_header.credit_days
        payment_method = purchase_header.payment_method
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        description = request.POST.get('description',False)
        date = datetime.date.today()
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        purchase_return_header = PurchaseReturnHeader(purchase_no = get_last_purchase_no, date = date, footer_description = description, payment_method = payment_method, credit_days = credit_days ,cartage_amount = cartage_amount, additional_tax = additional_tax, withholding_tax = 0, account_id = account_id, company_id = company, user_id = request.user )
        purchase_return_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = PurchaseReturnHeader.objects.get(purchase_no = get_last_purchase_no)
        for value in items:
            print(value["id"])
            item_id = Add_products.objects.get(id = value["id"])
            purchase_return_detail = PurchaseReturnDetail(item_id = item_id, quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], purchase_return_id = header_id)
            purchase_return_detail.save()
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            total_amount = item_amount + amount + float(cartage_amount) + float(additional_tax)
        header_id = header_id.id
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        if purchase_header.payment_method == 'Cash':
            company =  request.session['company']
            company = Company_info.objects.get(id = company)
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Return Invoice", amount = -abs(total_amount), date = date, remarks = "Amount Debit", copmany_id = company, user_id = request.user)
            tran2.save()
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Purchase Return Invoice", amount = total_amount, date = date, remarks = "Amount Debit", copmany_id = company, user_id = request.user)
            tran1.save()
        else:
            company =  request.session['company']
            company = Company_info.objects.get(id = company)
            purchase_account = ChartOfAccount.objects.get(account_title = 'Purchase Returns')
            tran1 = Transactions(refrence_id = 0, refrence_date = date, account_id = account_id, tran_type = "", amount = total_amount, date = date, remarks = "Amount Debit",ref_inv_tran_id = header_id ,ref_inv_tran_type = "Purchase Return Invoice", user_id = request.user, copmany_id = company)
            tran1.save()
            tran2 = Transactions(refrence_id = 0, refrence_date = date, account_id = purchase_account, tran_type = "", amount = -abs(total_amount), date = date, remarks = "Amount Debit", ref_inv_tran_id = header_id ,ref_inv_tran_type = "Purchase Return Invoice", user_id = request.user, copmany_id = company)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/purchase_return.html',{'purchase_header':purchase_header, 'purchase_detail': purchase_detail,'pk':pk,'get_last_purchase_no':get_last_purchase_no,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_purchase_return_edit)
def edit_purchase_return(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    amount = 0
    item_amount = 0
    total_amount = 0
    purchase_header = PurchaseReturnHeader.objects.filter(company, id = pk).first()
    purchase_detail = PurchaseReturnDetail.objects.filter(purchase_return_id = purchase_header.id).all()
    all_accounts = ChartOfAccount.objects.all()
    if request.method == 'POST':
        purchase_detail.delete()
        purchase_id = purchase_header.purchase_no
        supplier = request.POST.get('supplier',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        description = request.POST.get('description',False)
        date = datetime.date.today()
        account_id = ChartOfAccount.objects.get(account_title = supplier)
        purchase_header.footer_description = description
        purchase_header.account_id = account_id
        purchase_header.cartage_amount = cartage_amount
        purchase_header.additional_tax = additional_tax

        purchase_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = PurchaseReturnHeader.objects.get(purchase_no = purchase_id)
        for value in items:
            item_id = Add_products.objects.get(id = value["id"])
            purchase_return_detail = PurchaseReturnDetail(item_id = item_id, quantity = value["quantity"] ,cost_price = value["price"], retail_price = 0.00, sales_tax = value["sales_tax"], purchase_return_id = header_id)
            purchase_return_detail.save()
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            total_amount = item_amount + amount + float(cartage_amount) + float(additional_tax)
        header_id = header_id.id
        refrence_id = Q(refrence_id = header_id)
        tran_type = Q(tran_type = "Purchase Return Invoice")
        delete = Transactions.objects.filter(refrence_id, tran_type)
        delete.delete()
        purchase_account = ChartOfAccount.objects.get(account_title = 'Purchase Returns')
        if purchase_header.payment_method == 'Cash':
            company =  request.session['company']
            company = Company_info.objects.get(id = company)
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Return Invoice", amount = -abs(total_amount), date = date, remarks = "Amount Credit", company = company_id, user_id = request.user)
            tran2.save()
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Purchase Return Invoice", amount = total_amount, date = date, remarks = "Amount Debit", company = company_id, user_id = request.user)
            tran1.save()
        else:
            purchase_account = ChartOfAccount.objects.get(account_title = 'Purchase Returns')
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Purchase Return Invoice", amount = total_amount, date = date, remarks = "Amount Debit", company = company_id, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = purchase_account, tran_type = "Purchase Return Invoice", amount = -abs(total_amount), date = date, remarks = "Amount Debit", company = company_id, user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/edit_purchase_return.html',{'purchase_header':purchase_header, 'purchase_detail': purchase_detail,'pk':pk,'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_sale_display)
def sale(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = sale_roles(request.user)
    all_sales = SaleHeader.objects.filter(company).all()
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    gst = Company_info.objects.filter(id = company.id).first()
    return render(request, 'transaction/sale.html',{'all_sales': all_sales,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser,'gst':gst})


@login_required
@user_passes_test(allow_sale_add)
def new_sale(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    item_amount = 0
    total_amount = 0
    get_account = ''
    ca = 0
    cartage_sum = 0
    cursor = connection.cursor()
    customer_name_sale = request.POST.get('customer_name_sale')
    if customer_name_sale:
        try:
            get_account = ChartOfAccount.objects.get(account_title = customer_name_sale)
            if get_account:
                customer_dc = cursor.execute('''Select Distinct id,dc_no,accountid,account_title From (
                                            Select distinct dc_id_id,COA.id As accountid,COA.account_title,IP.product_code,IP.product_name,
                                            DC.Quantity As DcQuantity,ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                            (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                                            from customer_dcdetailcustomer DC
                                            inner join customer_dcHeadercustomer HDDC on DC.dc_id_id = HDDC.id
                                            inner join transaction_chartofaccount COA on HDDC.account_id_id = COA.id
                                            inner join inventory_add_products IP on DC.item_id_id = IP.id
                                            Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                            And SD.item_id_id = IP.id
                                            group by dc_id_id,COA.id,COA.account_title,IP.product_code,IP.product_name
                                            ) As tblData
                                            Inner Join customer_dcheadercustomer HD on  HD.id = tblData.dc_id_id
                                            Where RemainingQuantity > 0 AND accountid = %s AND HD.company_id_id = %s ''',[get_account.id, company.id])
                customer_dc = customer_dc.fetchall()
                print("here", customer_dc)
                return JsonResponse({'customer_dc':customer_dc})
        except ObjectDoesNotExist:
            return JsonResponse({'customer_dc':'False'})

    all_dc = request.POST.get('all_dc')
    if all_dc:
        all_dc = cursor.execute('''Select Distinct id,dc_no,accountid,account_title From (
                                Select distinct dc_id_id,COA.id As accountid,COA.account_title,IP.product_code,IP.product_name,
                                DC.Quantity As DcQuantity,ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                                from customer_dcdetailcustomer DC
                                inner join customer_dcHeadercustomer HDDC on DC.dc_id_id = HDDC.id
                                inner join transaction_chartofaccount COA on HDDC.account_id_id = COA.id
                                inner join inventory_add_products IP on DC.item_id_id = IP.id
                                Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                And SD.item_id_id = IP.id
                                group by dc_id_id,COA.id,COA.account_title,IP.product_code,IP.product_name
                                ) As tblData
                                Inner Join customer_dcheadercustomer HD on  HD.id = tblData.dc_id_id
                                Where RemainingQuantity > 0 AND HD.company_id_id = %s ''',[company.id])
        all_dc = all_dc.fetchall()
        return JsonResponse({'all_dc':all_dc})

    customer = Q(account_id = "100")
    supplier = Q(account_id = "200")
    all_accounts = ChartOfAccount.objects.filter(customer|supplier).all()
    get_last_sale_no = SaleHeader.objects.filter(company_id = company.id).last()

    if company.id == 1:
        if get_last_sale_no:
            get_last_sale_no = get_last_sale_no.sale_no
            num = int(get_last_sale_no)
            num = num + 1
            get_last_sale_no = str(num)
        else:
            get_last_sale_no = '8232'
    else:
        if get_last_sale_no:
            get_last_sale_no = get_last_sale_no.sale_no
            num = int(get_last_sale_no)
            num = num + 1
            get_last_sale_no = str(num)
        else:
            get_last_sale_no = '101'
    dc_code_sale = request.POST.get('dc_code_sale',False)
    if dc_code_sale:
        header_id = DcHeaderCustomer.objects.filter(company_id = company.id).get(dc_no = dc_code_sale)
        data = cursor.execute('''Select * From (
                                Select distinct SD.id as Sd_detail_id,dc_id_id,IP.id,IP.product_code,IP.product_name, IP.product_desc, IP.unit,
                                DC.Quantity As DcQuantity,
                                ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity, DC.id as Dc_detail_id
                                from customer_dcdetailcustomer DC
                                inner join inventory_add_products IP on IP.id = DC.item_id_id
                                Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                And SD.item_id_id = IP.id
                                group by SD.id,DC.id
                                ) As tblData
                                Where RemainingQuantity > 0 And dc_id_id = %s
                            ''',[header_id.id])
        row = data.fetchall()
        return JsonResponse({"row":row,'dc_ref':header_id.id})
    # get_item_code = request.POST.get('item_code', False)
    # quantity = request.POST.get('quantity', False)
    # if get_item_code:
    #     cursor = connection.cursor()
    #     cursor.execute('''Select item_code, item_name,Item_description,Unit,SUM(quantity) As qty From (
    #                     Select 'Opening Stock' As TranType,Product_Code As Item_Code,Product_Name As Item_name,Product_desc As Item_description,Unit As unit,Opening_Stock as Quantity From inventory_add_products
    #                     where product_code = %s
    #                     union All
    #                     Select 'Purchase' As TranType,Item_Code,Item_name,Item_description,unit,Quantity From transaction_purchasedetail
    #                     where item_code = %s
    #                     union All
    #                     Select 'Purchase Return' As TranType,Item_Code,Item_name,Item_description,unit,Quantity * -1 From transaction_purchasereturndetail
    #                     where item_code = %s
    #                     union All
    #                     Select 'Sale' As TranType,Item_Code,Item_name,Item_description,unit,Quantity * -1 From transaction_saledetail
    #                     where item_code = %s
    #                     union All
    #                     Select 'Sale Return' As TranType,Item_Code,Item_name,Item_description,unit,Quantity  From transaction_salereturndetail
    #                     where item_code = %s
    #                     ) As tblTemp
    #                     Group by Item_Code''',[get_item_code,get_item_code,get_item_code,get_item_code,get_item_code])
    #     row = cursor.fetchall()
    #     a = row[0][4]
    #     b = quantity
    #     if str(a) > str(b):
    #         print(quantity)
    #         print(row[0][4])
    #         return JsonResponse({"message":"True"})
    #     else:
    #         return JsonResponse({"message":"False"})
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id',False)
        date = request.POST.get('date',False)
        customer = request.POST.get('customer',False)
        follow_up = request.POST.get('follow_up',False)
        credit_days = request.POST.get('credit_days',False)
        payment_method = request.POST.get('payment_method',False)
        hs_code = request.POST.get('hs_code',False)
        footer_desc = request.POST.get('footer_desc',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        withholding_tax = request.POST.get('withholding_tax',False)
        account_id = ChartOfAccount.objects.get(account_title = customer)

        if follow_up:
            follow_up = follow_up
        else:
            follow_up = '2010-06-10'
        sale_header = SaleHeader(sale_no = sale_id, date = date, footer_description = footer_desc, payment_method = payment_method, cartage_amount = cartage_amount, additional_tax = additional_tax, withholding_tax = withholding_tax, account_id = account_id, follow_up = follow_up, credit_days = credit_days, company_id = company, user_id = request.user, hs_code = hs_code)
        cart = json.loads(request.POST.get('cartage'))
        items = json.loads(request.POST.get('items'))
        sale_header.save()
        header_id = SaleHeader.objects.filter(company_id = company.id).get(sale_no = sale_id)
        for value in cart:
            cartage_ = Cartage_and_Po(cartage = value["cartage_amount"], po_no = value["po_no"], invoice_id = header_id.id)
            cartage_.save()
            cartage_sum = cartage_sum + float(value["cartage_amount"])
        for value in items:
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
            item_amount = item_amount + float(additional_tax)
            item_id = Add_products.objects.get(id = value["id"])
            sale_detail = SaleDetail(item_id = item_id,  quantity = value["quantity"],cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], dc_ref = value["dc_no"], sale_id = header_id, total = amount)
            sale_detail.save()
        total_amount = item_amount
        total_amount = total_amount + cartage_sum
        header_id = header_id.id
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        if payment_method == 'Cash':
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Sale Invoice", amount = total_amount, date = date, remarks = sale_id,  ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = sale_id,   ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran2.save()
        else:
            sale_account = ChartOfAccount.objects.get(account_title = 'Sales')
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Invoice", amount = total_amount, date = date, remarks = sale_id,  ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = sale_account, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = sale_id,ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/new_sales.html',{'get_last_sale_no':get_last_sale_no, 'all_accounts':all_accounts, 'all_dc':all_dc,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
def direct_sale(request, pk):
    cartage_sum = 0
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    dc_header = DcHeaderCustomer.objects.filter(id = pk).first()
    header_id = DcHeaderCustomer.objects.get(id = pk)
    cursor = connection.cursor()
    dc_detail = cursor.execute('''Select * From (
                                Select distinct dc_id_id,IP.id,IP.product_code,IP.product_name, IP.product_desc, IP.unit,
                                DC.Quantity As DcQuantity,
                                ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                                from customer_dcdetailcustomer DC
                                inner join inventory_add_products IP on IP.id = DC.item_id_id
                                Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                And SD.item_id_id = IP.id
                                group by dc_id_id,ip.product_code,ip.product_name
                                ) As tblData
                                Where RemainingQuantity > 0 And dc_id_id = %s ''',[header_id.id])
    dc_detail = dc_detail.fetchall()
    item_amount = 0
    total_amount = 0
    all_item_code = Add_products.objects.all()
    all_accounts = ChartOfAccount.objects.all()
    get_last_sale_no = SaleHeader.objects.last()
    if get_last_sale_no:
        get_last_sale_no = get_last_sale_no.sale_no
        num = int(get_last_sale_no)
        num = num + 1
        get_last_sale_no = str(num)
    else:
        get_last_sale_no = '8232'
    item_code = request.POST.get('item_code_sale',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id',False)
        customer = request.POST.get('customer',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        hs_code = request.POST.get('hs_code',False)
        additional_tax = request.POST.get('additional_tax',False)
        account_id = ChartOfAccount.objects.get(account_title = customer)
        date = datetime.date.today()

        sale_header = SaleHeader(sale_no = sale_id, date = date, footer_description = footer_desc, payment_method = payment_method, cartage_amount = 0.00, additional_tax = additional_tax, withholding_tax = 0.00, account_id = account_id, follow_up = '2010-06-10', company_id = company, user_id = request.user, hs_code = hs_code)
        items = json.loads(request.POST.get('items'))
        cart = json.loads(request.POST.get('cartage'))
        sale_header.save()
        header_id = SaleHeader.objects.get(sale_no = sale_id)
        for value in cart:
            cartage_ = Cartage_and_Po(cartage = value["cartage_amount"], po_no = value["po_no"], invoice_id = header_id.id)
            cartage_.save()
            cartage_sum = cartage_sum + float(value["cartage_amount"])
        for value in items:
            item_id = Add_products.objects.get(id = value["id"])
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
            sale_detail = SaleDetail(item_id = item_id,  quantity = value["quantity"],cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], dc_ref = value["dc_no"], sale_id = header_id, total = amount)
            sale_detail.save()
        item_amount = item_amount + float(additional_tax)
        total_amount = item_amount
        header_id = header_id.id
        total_amount = total_amount + cartage_sum
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        if payment_method == 'Cash':
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Sale Invoice", amount = total_amount, date = date, remarks = sale_id,  ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = sale_id,   ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran2.save()
        else:
            sale_account = ChartOfAccount.objects.get(account_title = 'Sales')
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Invoice", amount = total_amount, date = date, remarks = sale_id,  ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = sale_account, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = sale_id,ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/direct_invoice.html',{'all_item_code':all_item_code,'get_last_sale_no':get_last_sale_no, 'all_accounts':all_accounts, 'dc_header':dc_header, 'dc_detail':dc_detail, 'pk':pk,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_sale_edit)
def edit_sale(request,pk):
    ca = 0
    cartage_sum = 0
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    item_amount = 0
    total_amount = 0
    cursor = connection.cursor()
    all_item_code = Add_products.objects.all()
    sale_header = SaleHeader.objects.filter(company, id = pk).first()
    cartages = Cartage_and_Po.objects.filter(invoice_id = sale_header.id).all()
    sale_detail = SaleDetail.objects.filter(sale_id = sale_header.id).all()
    customer = Q(account_id = "100")
    supplier = Q(account_id = "200")
    all_accounts = ChartOfAccount.objects.filter(customer|supplier).all()
    customer_name_sale = request.POST.get('customer_name_sale')
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    if customer_name_sale:
        try:
            get_account = ChartOfAccount.objects.get(account_title = customer_name_sale)
            if get_account:
                customer_dc = cursor.execute('''Select Distinct id,dc_no,accountid,account_title From (
                                            Select distinct dc_id_id,COA.id As accountid,COA.account_title,IP.product_code,IP.product_name,
                                            DC.Quantity As DcQuantity,ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                            (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                                            from customer_dcdetailcustomer DC
                                            inner join customer_dcHeadercustomer HDDC on DC.dc_id_id = HDDC.id
                                            inner join transaction_chartofaccount COA on HDDC.account_id_id = COA.id
                                            inner join inventory_add_products IP on DC.item_id_id = IP.id
                                            Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                            And SD.item_id_id = IP.id
                                            group by dc_id_id,COA.id,COA.account_title,IP.product_code,IP.product_name
                                            ) As tblData
                                            Inner Join customer_dcheadercustomer HD on  HD.id = tblData.dc_id_id
                                            Where RemainingQuantity > 0 AND accountid = %s AND HD.company_id_id = %s ''',[get_account.id, company.id])
                customer_dc = customer_dc.fetchall()
                return JsonResponse({'customer_dc':customer_dc})
        except ObjectDoesNotExist:
            return JsonResponse({'customer_dc':'False'})

    all_dc = request.POST.get('all_dc')
    if all_dc:
        all_dc = cursor.execute('''Select Distinct id,dc_no,accountid,account_title From (
                                Select distinct dc_id_id,COA.id As accountid,COA.account_title,IP.product_code,IP.product_name,
                                DC.Quantity As DcQuantity,ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                                from customer_dcdetailcustomer DC
                                inner join customer_dcHeadercustomer HDDC on DC.dc_id_id = HDDC.id
                                inner join transaction_chartofaccount COA on HDDC.account_id_id = COA.id
                                inner join inventory_add_products IP on DC.item_id_id = IP.id
                                Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                And SD.item_id_id = IP.id
                                group by dc_id_id,COA.id,COA.account_title,IP.product_code,IP.product_name
                                ) As tblData
                                Inner Join customer_dcheadercustomer HD on  HD.id = tblData.dc_id_id
                                Where RemainingQuantity > 0 AND HD.company_id_id = %s ''',[company.id])
        all_dc = all_dc.fetchall()
        return JsonResponse({'all_dc':all_dc})
    dc_code_sale = request.POST.get('dc_code_sale')
    if dc_code_sale:
        header_id = DcHeaderCustomer.objects.filter(company_id = company.id).get(dc_no = dc_code_sale)
        data = cursor.execute('''Select * From (
                            Select distinct dc_id_id,IP.id,IP.product_code,IP.product_name, IP.product_desc, IP.unit,
                            DC.Quantity As DcQuantity,
                            ifnull(sum(SD.Quantity),0) As SaleQuantity,
                            (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                            from customer_dcdetailcustomer DC
                            inner join inventory_add_products IP on IP.id = DC.item_id_id
                            Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                            And SD.item_id_id = IP.id
                            group by dc_id_id,IP.product_code,IP.product_name
                            ) As tblData
                            Where RemainingQuantity > 0 And dc_id_id = %s
                            ''',[header_id.id])
        row = data.fetchall()
        return JsonResponse({"row":row,'dc_ref':header_id.id})
    if request.method == 'POST':
        sale_detail.delete()

        sale_id = request.POST.get('sale_id',False)
        customer = request.POST.get('customer',False)
        credit_days = request.POST.get('credit_days',False)
        follow_up = request.POST.get('follow_up',False)
        hs_code = request.POST.get('hs_code',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        withholding_tax = request.POST.get('withholding_tax',False)
        account_id = ChartOfAccount.objects.get(account_title = customer)
        date = datetime.date.today()

        if follow_up:
            follow_up = follow_up
        else:
            follow_up = '2010-06-10'

        sale_header.follow_up = follow_up
        sale_header.credit_days = credit_days
        sale_header.payment_method = payment_method
        sale_header.footer_description = footer_desc
        sale_header.cartage_amount = cartage_amount
        sale_header.additional_tax = additional_tax
        sale_header.withholding_tax = withholding_tax
        sale_header.account_id = account_id
        sale_header.hs_code = hs_code

        sale_header.save()

        cart = json.loads(request.POST.get('cartage'))
        items = json.loads(request.POST.get('items'))
        sale_header.save()
        header_id = SaleHeader.objects.filter(company_id = company.id).get(sale_no = sale_id)
        Cartage_and_Po.objects.filter(invoice_id = header_id.id).all().delete()
        for value in cart:
            cartage_ = Cartage_and_Po(cartage = value["cartage_amount"], po_no = value["po_no"], invoice_id = header_id.id)
            cartage_.save()
            cartage_sum = cartage_sum + float(value["cartage_amount"])
        for value in items:
            company =  request.session['company']
            company = Company_info.objects.get(id = company)
            item_id = Add_products.objects.get(id = value["id"])
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
            sale_detail = SaleDetail(item_id = item_id, quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], sale_id = header_id, dc_ref = value["dc_no"], total = amount)
            sale_detail.save()
        item_amount = item_amount + float(additional_tax)
        total_amount = item_amount
        header_id = header_id.id
        total_amount = total_amount + cartage_sum
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        if sale_header.payment_method == 'Cash':
            refrence_id = Q(refrence_id = header_id)
            tran_type = Q(tran_type = "Sale Invoice")
            delete = Transactions.objects.filter(refrence_id, tran_type)
            delete.delete()
            tran1 = Transactions(refrence_id = header_id, refrence_date = sale_header.date, account_id = cash_in_hand, tran_type = "Sale Invoice", amount = total_amount, date = date, ref_inv_tran_id = 0, ref_inv_tran_type = "" ,remarks = sale_id, company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = sale_header.date, account_id = account_id, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = sale_id,  ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran2.save()
        else:
            refrence_id = Q(refrence_id = header_id)
            tran_type = Q(tran_type = "Sale Invoice")
            delete = Transactions.objects.filter(refrence_id, tran_type)
            delete.delete()
            sale_account = ChartOfAccount.objects.get(account_title = 'Sales')
            tran1 = Transactions(refrence_id = header_id, refrence_date = sale_header.date, account_id = account_id, tran_type = "Sale Invoice", amount = total_amount, date = date, remarks = sale_id, ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = sale_header.date, account_id = sale_account, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = sale_id, ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/edit_sale.html',{'all_item_code':all_item_code,'all_accounts':all_accounts, 'sale_header':sale_header, 'sale_detail':sale_detail, 'pk':pk, 'all_dc':all_dc,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser,'cartages':cartages})



def voucher_avaliable_sale(pk):
    cusror = connection.cursor()
    row = cusror.execute('''select case
                            when exists (select id from transaction_voucherdetail  where  invoice_id = %s)
                            then 'y'
                            else 'n'
                            end''',[pk])
    row = row.fetchall()
    res_list = [x[0] for x in row]
    if res_list[0] == "n":
        refrence_id = Q(refrence_id = pk)
        tran_type = Q(tran_type = "Sale Invoice")
        ref_inv_tran_id = Q(ref_inv_tran_id = pk)
        ref_inv_tran_type = Q(ref_inv_tran_type = "Sale CRV")
        Transactions.objects.filter(refrence_id , tran_type).all().delete()
        Transactions.objects.filter(ref_inv_tran_id , ref_inv_tran_type).all().delete()
        SaleDetail.objects.filter(sale_id = pk).all().delete()
        SaleHeader.objects.filter(id = pk).delete()
        return True
    else:
        return False

@login_required
@user_passes_test(allow_sale_delete)
def delete_sale(request, pk):
    item = voucher_avaliable_sale(pk)
    if item == True:
        messages.add_message(request, messages.SUCCESS, "Sale Invoice Deleted.")
        return redirect('sale')
    else:
        messages.add_message(request, messages.ERROR, "You cannot delete this Invoice, kindly delet it's voucher first.")
        return redirect('sale')

@login_required
@user_passes_test(allow_sale_add)
def new_sale_non_gst(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    item_amount = 0
    total_amount = 0
    get_account = ''
    ca = 0
    cartage_sum = 0
    cursor = connection.cursor()

    # dc_detail = cursor.execute('''Select Distinct id,item_code, item_name, item_description From (
    #                             Select distinct dc_id_id,DC.item_code,DC.Item_name,DC.Item_description,
    #                             DC.Quantity As DcQuantity,
    #                             ifnull(sum(SD.Quantity),0) As SaleQuantity,
    #                             (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
    #                             from customer_dcdetailcustomer DC
    #                             Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
    #                             And SD.item_code = DC.item_code
    #                             group by dc_id_id,dc.item_code,dc.Item_name
    #                             ) As tblData
    #                             Inner Join customer_dcheadercustomer  HD on  HD.id = tblData.dc_id_id
    #                             Where RemainingQuantity > 0
    #                             group by tblData.item_code''')
    # dc_detail = dc_detail.fetchall()

    customer_name_sale = request.POST.get('customer_name_sale')
    if customer_name_sale:
        try:
            get_account = ChartOfAccount.objects.get(account_title = customer_name_sale)
            if get_account:
                customer_dc = cursor.execute('''Select Distinct id,dc_no,accountid,account_title From (
                                            Select distinct dc_id_id,COA.id As accountid,COA.account_title,IP.product_code,IP.product_name,
                                            DC.Quantity As DcQuantity,ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                            (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                                            from customer_dcdetailcustomer DC
                                            inner join customer_dcHeadercustomer HDDC on DC.dc_id_id = HDDC.id
                                            inner join transaction_chartofaccount COA on HDDC.account_id_id = COA.id
                                            inner join inventory_add_products IP on DC.item_id_id = IP.id
                                            Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                            And SD.item_id_id = IP.id
                                            group by dc_id_id,COA.id,COA.account_title,IP.product_code,IP.product_name
                                            ) As tblData
                                            Inner Join customer_dcheadercustomer HD on  HD.id = tblData.dc_id_id
                                            Where RemainingQuantity > 0 AND accountid = %s AND HD.company_id_id = %s ''',[get_account.id, company.id])
                customer_dc = customer_dc.fetchall()
                return JsonResponse({'customer_dc':customer_dc})
        except ObjectDoesNotExist:
            return JsonResponse({'customer_dc':'False'})

    all_dc = request.POST.get('all_dc')
    if all_dc:
        all_dc = cursor.execute('''Select Distinct id,dc_no,accountid,account_title From (
                                Select distinct dc_id_id,COA.id As accountid,COA.account_title,IP.product_code,IP.product_name,
                                DC.Quantity As DcQuantity,ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                                from customer_dcdetailcustomer DC
                                inner join customer_dcHeadercustomer HDDC on DC.dc_id_id = HDDC.id
                                inner join transaction_chartofaccount COA on HDDC.account_id_id = COA.id
                                inner join inventory_add_products IP on DC.item_id_id = IP.id
                                Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                And SD.item_id_id = IP.id
                                group by dc_id_id,COA.id,COA.account_title,IP.product_code,IP.product_name
                                ) As tblData
                                Inner Join customer_dcheadercustomer HD on  HD.id = tblData.dc_id_id
                                Where RemainingQuantity > 0 AND HD.company_id_id = %s ''',[company.id])
        all_dc = all_dc.fetchall()
        return JsonResponse({'all_dc':all_dc})
    customer = Q(account_id = "100")
    supplier = Q(account_id = "200")
    all_accounts = ChartOfAccount.objects.filter(customer|supplier).all()
    get_last_sale_no = SaleHeader.objects.filter(company_id = company.id).last()
    if get_last_sale_no:
        get_last_sale_no = get_last_sale_no.sale_no
        num = int(get_last_sale_no)
        num = num + 1
        get_last_sale_no = str(num)
    else:
        get_last_sale_no = '101'
    dc_code_sale = request.POST.get('dc_code_sale',False)
    if dc_code_sale:

        header_id = DcHeaderCustomer.objects.filter(company_id = company.id).get(dc_no = dc_code_sale)
        data = cursor.execute('''Select * From (
                            Select distinct dc_id_id,IP.id,IP.product_code,IP.product_name, IP.product_desc, IP.unit,
                            DC.Quantity As DcQuantity,
                            ifnull(sum(SD.Quantity),0) As SaleQuantity,
                            (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                            from customer_dcdetailcustomer DC
                            inner join inventory_add_products IP on IP.id = DC.item_id_id
                            Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                            And SD.item_id_id = IP.id
                            group by dc_id_id,IP.product_code,IP.product_name
                            ) As tblData
                            Where RemainingQuantity > 0 And dc_id_id = %s
                            ''',[header_id.id])
        row = data.fetchall()
        return JsonResponse({"row":row,'dc_ref':header_id.id})
    # get_item_code = request.POST.get('item_code', False)
    # quantity = request.POST.get('quantity', False)
    # if get_item_code:
    #     cursor = connection.cursor()
    #     cursor.execute('''Select item_code, item_name,Item_description,Unit,SUM(quantity) As qty From (
    #                     Select 'Opening Stock' As TranType,Product_Code As Item_Code,Product_Name As Item_name,Product_desc As Item_description,Unit As unit,Opening_Stock as Quantity From inventory_add_products
    #                     where product_code = %s
    #                     union All
    #                     Select 'Purchase' As TranType,Item_Code,Item_name,Item_description,unit,Quantity From transaction_purchasedetail
    #                     where item_code = %s
    #                     union All
    #                     Select 'Purchase Return' As TranType,Item_Code,Item_name,Item_description,unit,Quantity * -1 From transaction_purchasereturndetail
    #                     where item_code = %s
    #                     union All
    #                     Select 'Sale' As TranType,Item_Code,Item_name,Item_description,unit,Quantity * -1 From transaction_saledetail
    #                     where item_code = %s
    #                     union All
    #                     Select 'Sale Return' As TranType,Item_Code,Item_name,Item_description,unit,Quantity  From transaction_salereturndetail
    #                     where item_code = %s
    #                     ) As tblTemp
    #                     Group by Item_Code''',[get_item_code,get_item_code,get_item_code,get_item_code,get_item_code])
    #     row = cursor.fetchall()
    #     a = row[0][4]
    #     b = quantity
    #     if str(a) > str(b):
    #         print(quantity)
    #         print(row[0][4])
    #         return JsonResponse({"message":"True"})
    #     else:
    #         return JsonResponse({"message":"False"})
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id',False)
        customer = request.POST.get('customer',False)
        follow_up = request.POST.get('follow_up',False)
        credit_days = request.POST.get('credit_days',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        account_id = ChartOfAccount.objects.get(account_title = customer)
        date = datetime.date.today()

        if follow_up:
            follow_up = follow_up
        else:
            follow_up = '2010-06-10'

        sale_header = SaleHeader(sale_no = sale_id, date = date, footer_description = footer_desc, payment_method = payment_method, cartage_amount = 0.00, additional_tax = 0.00, withholding_tax = 0.00, account_id = account_id, follow_up = follow_up, credit_days = credit_days, company_id = company, user_id = request.user)
        cart = json.loads(request.POST.get('cartage'))
        items = json.loads(request.POST.get('items'))
        sale_header.save()
        header_id = SaleHeader.objects.filter(company_id = company.id).get(sale_no = sale_id)
        print(cart)
        for value in cart:
            cartage_ = Cartage_and_Po(cartage = value["cartage_amount"], po_no = value["po_no"], invoice_id = header_id.id)
            cartage_.save()
            cartage_sum = cartage_sum + float(value["cartage_amount"])
            print(cartage_sum)
        for value in items:
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            amount = quantity * price
            item_amount = item_amount + amount
            item_id = Add_products.objects.get(id = value["id"])
            sale_detail = SaleDetail(item_id = item_id,  quantity = value["quantity"],cost_price = value["price"], retail_price = 0, sales_tax = 0, dc_ref = value["dc_no"], sale_id = header_id, total = amount)
            sale_detail.save()
        total_amount = item_amount
        header_id = header_id.id
        total_amount = total_amount + cartage_sum
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        if payment_method == 'Cash':
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Sale Invoice", amount = total_amount, date = date, remarks = "Amount Debit",  ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = "Amount Debit",   ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran2.save()
        else:
            sale_account = ChartOfAccount.objects.get(account_title = 'Sales')
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Invoice", amount = total_amount, date = date, remarks = "Amount Debit",  ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = sale_account, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = "Amount Debit",ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/new_sale_non_gst.html',{'get_last_sale_no':get_last_sale_no, 'all_accounts':all_accounts, 'all_dc':all_dc,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
def direct_sale_non_gst(request, pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    dc_header = DcHeaderCustomer.objects.filter(id = pk).first()
    header_id = DcHeaderCustomer.objects.get(id = pk)
    cursor = connection.cursor()
    dc_detail = cursor.execute('''Select * From (
                                Select distinct dc_id_id,IP.id,IP.product_code,IP.product_name, IP.product_desc, IP.unit,
                                DC.Quantity As DcQuantity,
                                ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                                from customer_dcdetailcustomer DC
                                inner join inventory_add_products IP on IP.id = DC.item_id_id
                                Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                And SD.item_id_id = IP.id
                                group by dc_id_id,ip.product_code,ip.product_name
                                ) As tblData
                                Where RemainingQuantity > 0 And dc_id_id = %s ''',[header_id.id])
    dc_detail = dc_detail.fetchall()
    item_amount = 0
    total_amount = 0
    all_item_code = Add_products.objects.all()
    all_accounts = ChartOfAccount.objects.all()
    get_last_sale_no = SaleHeader.objects.last()
    if get_last_sale_no:
        get_last_sale_no = get_last_sale_no.sale_no
        get_last_sale_no = get_last_sale_no[-3:]
        num = int(get_last_sale_no)
        num = num + 1
        get_last_sale_no = 'SAL/' + str(num)
    else:
        get_last_sale_no = 'SAL/101'
    item_code = request.POST.get('item_code_sale',False)
    if item_code:
        data = Add_products.objects.filter(product_code = item_code)
        row = serializers.serialize('json',data)
        return HttpResponse(json.dumps({'row':row}))
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id',False)
        customer = request.POST.get('customer',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        withholding_tax = request.POST.get('withholding_tax',False)
        account_id = ChartOfAccount.objects.get(account_title = customer)
        date = datetime.date.today()

        sale_header = SaleHeader(sale_no = sale_id, date = date, footer_description = footer_desc, payment_method = payment_method, cartage_amount = cartage_amount, additional_tax = additional_tax, withholding_tax = withholding_tax, account_id = account_id, follow_up = '2010-06-10', company_id = company, user_id = request.user)

        items = json.loads(request.POST.get('items'))
        cart = json.loads(request.POST.get('cartage'))
        sale_header.save()
        header_id = SaleHeader.objects.get(sale_no = sale_id)
        for value in items:
            item_id = Add_products.objects.get(id = value["id"])
            sale_detail = SaleDetail(item_id = item_id,  quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], dc_ref = value["dc_no"] ,sale_id = header_id, hs_code = value["hs_code"])
            sale_detail.save()
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
        item_amount = item_amount + float(cartage_amount) + float(additional_tax)
        total_amount = item_amount
        header_id = header_id.id
        cartage_amounts = cursor.execute('''Select SaleId,Cartage_amount ,DcNo,po_no,product_name, product_desc, unit, quantity, cost_price, sales_tax from(
                                    select SD.sale_id_id as SaleID, sum(DC.cartage_amount) as Cartage_amount, PS.id,PS.product_name as product_name, PS.product_desc as product_desc, PS.unit as unit,
                                    SD.quantity as quantity, SD.cost_price as cost_price, SD.sales_tax as sales_tax,
                                    DC.dc_no as DcNo, DCD.po_no  as po_no
                                    from transaction_saledetail SD
                                    inner join inventory_add_products PS on PS.id = SD.item_id_id
                                    inner join customer_dcheadercustomer DC on SD.dc_ref = DC.id
                                    inner join customer_dcdetailcustomer DCD on DCD.dc_id_id = DC.id
                                    left join customer_poheadercustomer PO on PO.id = DCD.po_no
                                    group by DCD.po_no
                                    )as tblData where tblData.SaleId = %s
                                    order by po_no''',[pk])
        cartage_amounts = cartage_amounts.fetchall()
        print(cartage_amounts)
        for c in cartage_amounts:
            ca = ca + c[1]
            print(ca)
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        if payment_method == 'Cash':
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Sale Invoice", amount = total_amount, date = date, remarks = "Amount Debit",ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = "Amount Debit",ref_inv_tran_id = 0, ref_inv_tran_type = "", company_id = company, user_id = request.user)
            tran2.save()
        else:
            sale_account = ChartOfAccount.objects.get(account_title = 'Sales')
            tran1 = Transactions(refrence_id = 0, refrence_date = date, account_id = account_id, tran_type = "", amount = total_amount, date = date, remarks = "Amount Debit",ref_inv_tran_id = header_id, ref_inv_tran_type = "Sale Invoice", company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = 0, refrence_date = date, account_id = sale_account, tran_type = "", amount = -abs(total_amount), date = date, remarks = "Amount Debit",ref_inv_tran_id = header_id, ref_inv_tran_type = "Sale Invoice", company_id = company, user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/direct_invoice_non_gst.html',{'all_item_code':all_item_code,'get_last_sale_no':get_last_sale_no, 'all_accounts':all_accounts, 'dc_header':dc_header, 'dc_detail':dc_detail, 'pk':pk,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_sale_edit)
def edit_sale_non_gst(request,pk):
    ca = 0
    cartage_sum = 0
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    item_amount = 0
    total_amount = 0
    cursor = connection.cursor()
    all_item_code = Add_products.objects.all()
    sale_header = SaleHeader.objects.filter(company, id = pk).first()
    cartages = Cartage_and_Po.objects.filter(invoice_id = sale_header.id).all()
    sale_detail = SaleDetail.objects.filter(sale_id = sale_header.id).all()
    all_accounts = ChartOfAccount.objects.all()
    customer_name_sale = request.POST.get('customer_name_sale')
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    if customer_name_sale:
        try:
            get_account = ChartOfAccount.objects.get(account_title = customer_name_sale)
            if get_account:
                customer_dc = cursor.execute('''Select Distinct id,dc_no,accountid,account_title From (
                                            Select distinct dc_id_id,COA.id As accountid,COA.account_title,IP.product_code,IP.product_name,
                                            DC.Quantity As DcQuantity,ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                            (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                                            from customer_dcdetailcustomer DC
                                            inner join customer_dcHeadercustomer HDDC on DC.dc_id_id = HDDC.id
                                            inner join transaction_chartofaccount COA on HDDC.account_id_id = COA.id
                                            inner join inventory_add_products IP on DC.item_id_id = IP.id
                                            Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                            And SD.item_id_id = IP.id
                                            group by dc_id_id,COA.id,COA.account_title,IP.product_code,IP.product_name
                                            ) As tblData
                                            Inner Join customer_dcheadercustomer HD on  HD.id = tblData.dc_id_id
                                            Where RemainingQuantity > 0 AND accountid = %s AND HD.company_id_id = %s ''',[get_account.id, company.id])
                customer_dc = customer_dc.fetchall()
                return JsonResponse({'customer_dc':customer_dc})
        except ObjectDoesNotExist:
            return JsonResponse({'customer_dc':'False'})

    all_dc = request.POST.get('all_dc')
    if all_dc:
        all_dc = cursor.execute('''Select Distinct id,dc_no,accountid,account_title From (
                                Select distinct dc_id_id,COA.id As accountid,COA.account_title,IP.product_code,IP.product_name,
                                DC.Quantity As DcQuantity,ifnull(sum(SD.Quantity),0) As SaleQuantity,
                                (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                                from customer_dcdetailcustomer DC
                                inner join customer_dcHeadercustomer HDDC on DC.dc_id_id = HDDC.id
                                inner join transaction_chartofaccount COA on HDDC.account_id_id = COA.id
                                inner join inventory_add_products IP on DC.item_id_id = IP.id
                                Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                                And SD.item_id_id = IP.id
                                group by dc_id_id,COA.id,COA.account_title,IP.product_code,IP.product_name
                                ) As tblData
                                Inner Join customer_dcheadercustomer HD on  HD.id = tblData.dc_id_id
                                Where RemainingQuantity > 0 AND HD.company_id_id = %s ''',[company.id])
        all_dc = all_dc.fetchall()
        return JsonResponse({'all_dc':all_dc})
    dc_code_sale = request.POST.get('dc_code_sale')
    if dc_code_sale:

        header_id = DcHeaderCustomer.objects.filter(company_id = company.id).get(dc_no = dc_code_sale)
        data = cursor.execute('''Select * From (
                            Select distinct dc_id_id,IP.id,IP.product_code,IP.product_name, IP.product_desc, IP.unit,
                            DC.Quantity As DcQuantity,
                            ifnull(sum(SD.Quantity),0) As SaleQuantity,
                            (DC.Quantity-ifnull(Sum(SD.Quantity),0)) As RemainingQuantity
                            from customer_dcdetailcustomer DC
                            inner join inventory_add_products IP on IP.id = DC.item_id_id
                            Left Join transaction_saledetail SD on SD.dc_ref = DC.dc_id_id
                            And SD.item_id_id = IP.id
                            group by dc_id_id,IP.product_code,IP.product_name
                            ) As tblData
                            Where RemainingQuantity > 0 And dc_id_id = %s
                            ''',[header_id.id])
        row = data.fetchall()
        return JsonResponse({"row":row,'dc_ref':header_id.id})
    if request.method == 'POST':
        sale_detail.delete()
        sale_id = request.POST.get('sale_id',False)
        customer = request.POST.get('customer',False)
        credit_days = request.POST.get('credit_days',False)
        follow_up = request.POST.get('follow_up',False)
        payment_method = request.POST.get('payment_method',False)
        footer_desc = request.POST.get('footer_desc',False)
        account_id = ChartOfAccount.objects.get(account_title = customer)
        date = datetime.date.today()

        if follow_up:
            follow_up = follow_up
        else:
            follow_up = '2010-06-10'

        sale_header.follow_up = follow_up
        sale_header.credit_days = credit_days
        sale_header.payment_method = payment_method
        sale_header.footer_description = footer_desc
        sale_header.account_id = account_id

        sale_header.save()

        cart = json.loads(request.POST.get('cartage'))
        items = json.loads(request.POST.get('items'))
        sale_header.save()
        header_id = SaleHeader.objects.filter(company_id = company.id).get(sale_no = sale_id)
        Cartage_and_Po.objects.filter(invoice_id = header_id.id).all().delete()
        for value in cart:
            cartage_ = Cartage_and_Po(cartage = value["cartage_amount"], po_no = value["po_no"], invoice_id = header_id.id)
            cartage_.save()
            cartage_sum = cartage_sum + float(value["cartage_amount"])
        for value in items:
            company =  request.session['company']
            company = Company_info.objects.get(id = company)
            item_id = Add_products.objects.get(id = value["id"])
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            amount = quantity * price
            item_amount = item_amount + amount
            sale_detail = SaleDetail(item_id = item_id, quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = 0, sale_id = header_id, dc_ref = value["dc_no"], total = amount)
            sale_detail.save()
        total_amount = item_amount
        header_id = header_id.id
        total_amount = total_amount + cartage_sum
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        if sale_header.payment_method == 'Cash':
            refrence_id = Q(refrence_id = header_id)
            tran_type = Q(tran_type = "Sale Invoice")
            delete = Transactions.objects.filter(refrence_id, tran_type)
            delete.delete()
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Sale Invoice", amount = total_amount, date = date, ref_inv_tran_id = 0, ref_inv_tran_type = "" ,remarks = "Amount Debit", company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = "Amount Debit",  ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran2.save()
        else:
            refrence_id = Q(refrence_id = header_id)
            tran_type = Q(tran_type = "Sale Invoice")
            delete = Transactions.objects.filter(refrence_id, tran_type)
            delete.delete()
            sale_account = ChartOfAccount.objects.get(account_title = 'Sales')
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Invoice", amount = total_amount, date = date, remarks = "Amount Debit", ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = sale_account, tran_type = "Sale Invoice", amount = -abs(total_amount), date = date, remarks = "Amount Debit", ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/edit_sale_ngst.html',{'all_item_code':all_item_code,'all_accounts':all_accounts, 'sale_header':sale_header, 'sale_detail':sale_detail, 'pk':pk, 'all_dc':all_dc,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser,'cartages':cartages})


def sale_return_summary(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    all_sales_return = SaleReturnHeader.objects.all()
    return render(request, 'transaction/sale_return_summary.html',{'all_sales_return': all_sales_return,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_sale_return_display)
def new_sale_return(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = sale_return_roles(request.user)
    item_amount = 0
    total_amount = 0
    get_last_sale_no = SaleReturnHeader.objects.last()
    if get_last_sale_no:
        get_last_sale_no = get_last_sale_no.sale_no
        get_last_sale_no = get_last_sale_no[-3:]
        num = int(get_last_sale_no)
        num = num + 1
        get_last_sale_no = 'SAL/RET/' + str(num)
    else:
        get_last_sale_no = 'SAL/RET/101'
    sale_header = SaleHeader.objects.filter(company, id = pk).first()
    sale_detail = SaleDetail.objects.filter(sale_id = sale_header.id).all()
    if request.method == 'POST':
        company =  request.session['company']
        company = Company_info.objects.get(id = company)
        customer = request.POST.get('customer',False)
        payment_method = request.POST.get('payment_method',False)
        description = request.POST.get('description',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        date = datetime.date.today()
        account_id = ChartOfAccount.objects.get(account_title = customer)
        sale_return_header = SaleReturnHeader(sale_no = get_last_sale_no, date = date, footer_description = description, payment_method = payment_method, cartage_amount = cartage_amount, additional_tax = additional_tax, withholding_tax = 0, account_id = account_id, company_id = company, user_id = request.user)
        sale_return_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = SaleReturnHeader.objects.get(sale_no = get_last_sale_no)
        for value in items:
            item_id = Add_products.objects.get(id = value["item_id"])
            sale_return_detail = SaleReturnDetail(item_id = item_id , quantity = value["quantity"], cost_price = value["price"], retail_price = 0, sales_tax = value["sales_tax"], sale_return_id = header_id)
            sale_return_detail.save()
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
        item_amount = item_amount + float(cartage_amount) + float(additional_tax)
        total_amount = item_amount
        header_id = header_id.id
        total_amount = total_amount
        cash_in_hand = ChartOfAccount.objects.get(account_title = 'Cash')
        if sale_header.payment_method == 'Cash':
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Sale Return Invoice", amount = -abs(total_amount), date = date, remarks = "",ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Return Invoice", amount = total_amount, date = date, remarks = "", ref_inv_tran_id = 0, ref_inv_tran_type = "" ,company_id = company, user_id = request.user)
            tran2.save()
        else:
            sale_return_account = ChartOfAccount.objects.get(account_title = 'Sales Returns')
            tran1 = Transactions(refrence_id = 0, refrence_date = date, account_id = account_id, tran_type = "", amount = -abs(total_amount), date = date, remarks = "",ref_inv_tran_id = header_id, ref_inv_tran_type = "Sale Invoice Return" ,company_id = company, user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = 0, refrence_date = date, account_id = sale_return_account, tran_type = "", amount = total_amount, date = date, remarks = "",ref_inv_tran_id = header_id, ref_inv_tran_type = "Sale Invoice Return" ,company_id = company, user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/sale_return.html',{'sale_header':sale_header, 'sale_detail': sale_detail,'pk':pk,'get_last_sale_no':get_last_sale_no,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_sale_return_edit)
def edit_sale_return(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    item_amount = 0
    total_amount = 0
    sale_header = SaleReturnHeader.objects.filter(company, id = pk).first()
    sale_detail = SaleReturnDetail.objects.filter(sale_return_id = sale_header.id).all()
    all_accounts = ChartOfAccount.objects.all()
    if request.method == 'POST':
        company =  request.session['company']
        company = Company_info.objects.get(id = company)
        sale_detail.delete()
        sale_id = request.POST.get('sale_id',False)
        customer = request.POST.get('customer',False)
        cartage_amount = request.POST.get('cartage_amount',False)
        additional_tax = request.POST.get('additional_tax',False)
        payment_method = request.POST.get('payment_method',False)
        description = request.POST.get('description',False)
        date = datetime.date.today()
        account_id = ChartOfAccount.objects.get(account_title = customer)
        sale_header.payment_method = payment_method
        sale_header.footer_description = description
        sale_header.account_id = account_id

        sale_header.save()
        items = json.loads(request.POST.get('items'))
        header_id = SaleReturnHeader.objects.get(sale_no = sale_header.sale_no)
        for value in items:
            item_id = Add_products.objects.get(id = value["id"])
            sale_return_detail = SaleReturnDetail(item_id = item_id, quantity = value["quantity"], cost_price = value["price"], retail_price = 0.00, sales_tax = value["sales_tax"], sale_return_id = header_id)
            sale_return_detail.save()
            quantity = float(value["quantity"])
            price =  float((value["price"]))
            sales_tax = float(value["sales_tax"])
            amount = (((quantity * price) * sales_tax) / 100)
            amount = ((quantity * price ) + amount)
            item_amount = item_amount + amount
        item_amount = item_amount + float(cartage_amount) + float(additional_tax)
        total_amount = item_amount
        header_id = header_id.id
        refrence_id = Q(refrence_id = header_id)
        tran_type = Q(tran_type = "Sale Return Invoice")
        delete = Transactions.objects.filter(refrence_id, tran_type)
        delete.delete()
        purchase_account = ChartOfAccount.objects.get(account_title = 'Sales Returns')
        if sale_header.payment_method == 'Cash':
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = cash_in_hand, tran_type = "Sale Return Invoice", amount = -abs(total_amount), date = date, remarks = "", company_id = company , user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Return Invoice", amount = total_amount, date = date, remarks = "", company_id = company , user_id = request.user)
            tran2.save()
        else:
            sale_return_account = ChartOfAccount.objects.get(account_title = 'Sales Returns')
            tran1 = Transactions(refrence_id = header_id, refrence_date = date, account_id = account_id, tran_type = "Sale Return Invoice", amount = -abs(total_amount), date = date, remarks = "", company_id = company , user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = header_id, refrence_date = date, account_id = sale_return_account, tran_type = "Sale Return Invoice", amount = total_amount, date = date, remarks = "", company_id = company , user_id = request.user)
            tran2.save()
        return JsonResponse({'result':'success'})
    return render(request, 'transaction/edit_sale_return.html',{'sale_header':sale_header, 'sale_detail': sale_detail,'pk':pk,'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_coa_display)
def chart_of_account(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = chart_account_roles(request.user)
    supplier = Q(account_id = '100')
    customer = Q(account_id = '200')
    bank = Q(account_id = '300')
    all_accounts = ChartOfAccount.objects.filter(supplier|customer|bank).all()
    if request.method == 'POST':
        account_title = request.POST.get('account_title')
        account_type = request.POST.get('account_type')
        opening_balance = request.POST.get('opening_balance')
        phone_no = request.POST.get('phone_no')
        email_address = request.POST.get('email_address')
        ntn = request.POST.get('ntn')
        stn = request.POST.get('stn')
        cnic = request.POST.get('cnic')
        address = request.POST.get('address')
        remarks = request.POST.get('remarks')
        op_type = request.POST.get('optradio')
        credit_limits = request.POST.get('credit_limits')

        if credit_limits is "":
            credit_limits = 0.00
        else:
            credit_limits = credit_limits

        if opening_balance is "":
            opening_balance = 0
        if op_type == "credit":
            opening_balance = -abs(Decimal(opening_balance))
        coa = ChartOfAccount(account_title = account_title, parent_id = account_type, opening_balance = opening_balance, phone_no = phone_no, email_address = email_address, ntn = ntn, stn = stn, cnic = cnic ,Address = address, remarks = remarks, credit_limit=credit_limits, account_id = "100")
        coa.save()
    return render(request, 'transaction/chart_of_account.html',{'all_accounts':all_accounts,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})

@login_required
@user_passes_test(allow_coa_edit)
def edit_chart_of_account(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        account_title = request.POST.get('account_title')
        account_type = request.POST.get('account_type')
        opening_balance = request.POST.get('opening_balance')
        phone_no = request.POST.get('phone_no')
        email_address = request.POST.get('email_address')
        ntn = request.POST.get('ntn')
        stn = request.POST.get('stn')
        cnic = request.POST.get('cnic')
        address = request.POST.get('address')
        remarks = request.POST.get('remarks')
        op_type = request.POST.get('optradio')
        credit_limits = request.POST.get('credit_limits')

        if credit_limits is "":
            credit_limits = 0.00
        else:
            credit_limits = credit_limits

        if opening_balance is "":
            opening_balance = 0
        if op_type == "credit":
            opening_balance = -abs(Decimal(opening_balance))
        coa = ChartOfAccount.objects.filter(id = id).first()
        coa.account_title = account_title
        coa.account_type = account_type
        coa.opening_balance = opening_balance
        coa.phone_no = phone_no
        coa.email_address = email_address
        coa.ntn = ntn
        coa.stn = stn
        coa.cnic = cnic
        coa.Address = address
        coa.remarks = remarks
        coa.credit_limit = credit_limits
        coa.save()
    return redirect('chart-of-account')


def account_transaction_avaliable(pk):
    cusror = connection.cursor()
    row = cusror.execute('''select case
                            when exists (select id from supplier_rfqsupplierheader  where account_id_id = %s)
                            or exists (select id from supplier_quotationheadersupplier  where account_id_id = %s)
                            or exists (select id from supplier_poheadersupplier  where account_id_id = %s)
                            or exists (select id from supplier_dcheadersupplier  where account_id_id = %s)
                            or exists (select id from customer_rfqcustomerheader  where account_id_id = %s)
                            or exists (select id from customer_quotationheadercustomer  where account_id_id = %s)
                            or exists (select id from customer_poheadercustomer  where account_id_id = %s)
                            or exists (select id from customer_dcheadercustomer  where account_id_id = %s)
                            or exists (select id from transaction_purchaseheader  where account_id_id = %s)
                            or exists (select id from transaction_purchasereturnheader  where account_id_id = %s)
                            or exists (select id from transaction_saleheader  where account_id_id = %s)
                            or exists (select id from transaction_salereturnheader  where account_id_id = %s)
                            or exists (select id from transaction_transactions  where account_id_id = %s)
                            or exists (select id from transaction_voucherdetail  where account_id_id = %s)
                            then 'y'
                            else 'n'
                            end
                            ''',[pk,pk,pk,pk,pk,pk,pk,pk,pk,pk,pk,pk,pk,pk])
    row = row.fetchall()
    res_list = [x[0] for x in row]
    if res_list[0] == "n":
        ChartOfAccount.objects.filter(id = pk).delete()
        return True
    else:
        return False

@login_required
def delete_chart_of_account(request,pk):
    account = account_transaction_avaliable(pk)
    if account == True:
        messages.add_message(request, messages.SUCCESS, "Account Deleted")
        return redirect('chart-of-account')
    else:
        messages.add_message(request, messages.ERROR, "You cannot delete this Account, it is refrenced")
        return redirect('chart-of-account')
    return redirect('chart-of-account')

@login_required
@user_passes_test(report_roles)
def reports(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    all_accounts = ChartOfAccount.objects.all()
    return render(request,'transaction/reports.html',{'all_accounts':all_accounts,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
def journal_voucher_summary(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = journal_voucher_roles(request.user)
    cursor = connection.cursor()
    all_voucher = cursor.execute('''select * from transaction_voucherheader where voucher_no LIKE '%JV%' ''')
    all_voucher = all_voucher.fetchall()
    return render(request, 'transaction/journal_voucher_summary.html',{'all_voucher':all_voucher,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'permission':permission,'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_jv_display)
def journal_voucher(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = journal_voucher_roles(request.user)
    cursor = connection.cursor()
    get_last_tran_id = cursor.execute('''select * from transaction_voucherheader where voucher_no LIKE '%%JV%%' AND company_id_id = %s order by voucher_no DESC LIMIT 1  ''',[company.id])
    get_last_tran_id = get_last_tran_id.fetchall()

    date = datetime.date.today()
    date = date.strftime('%Y%m')
    if get_last_tran_id:
        get_last_tran_id = get_last_tran_id[0][1]
        get_last_tran_id = get_last_tran_id[6:]
        print(get_last_tran_id)
        serial = str((int(get_last_tran_id) + 1))
        get_last_tran_id = date[2:]+'JV'+serial
    else:
        get_last_tran_id =  date[2:]+'JV1'

    account_id = request.POST.get('account_title',False)
    all_accounts = ChartOfAccount.objects.all()
    if account_id:
        account_info = ChartOfAccount.objects.filter(id = account_id).first()
        account_title = account_info.account_title
        account_id = account_info.id
        return JsonResponse({'account_title':account_title, 'account_id':account_id})
    all_invoices = SaleHeader.objects.filter(company_id = company.id).all()
    if request.method == "POST":
        check = request.POST.get('check', False)
        doc_no = request.POST.get('doc_no', False)
        doc_date = request.POST.get('doc_date', False)
        description = request.POST.get('description', False)
        items = json.loads(request.POST.get('items', False))
        invoice_id = SaleHeader.objects.filter(sale_no = doc_no, company_id = company.id).first()
        if invoice_id:
            invoice_id = invoice_id.id
        else:
            doc_no = doc_no
        date = datetime.date.today()
        jv_header = VoucherHeader(voucher_no = get_last_tran_id, date = date ,doc_no = doc_no, doc_date = doc_date, cheque_no = "-",cheque_date = doc_date, description = description, company_id = company, user_id = request.user)
        jv_header.save()
        voucher_id = VoucherHeader.objects.filter(company_id = company.id).get(voucher_no = get_last_tran_id)
        for value in items:
            account_id = ChartOfAccount.objects.get(account_title = value["account_title"])
            if value["debit"] > "0" and value["debit"] > "0.00":
                if check == "1":
                    tran1 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = abs(float(value["debit"])),
                                        date = datetime.date.today(), remarks = description, account_id = account_id, ref_inv_tran_id = invoice_id, ref_inv_tran_type = 'JV ST', voucher_id = voucher_id.id, company_id = company, user_id = request.user)
                else:
                    tran1 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = abs(float(value["debit"])),
                                        date = datetime.date.today(), remarks = description, account_id = account_id, ref_inv_tran_id = doc_no, ref_inv_tran_type = 'JV', voucher_id = voucher_id.id, company_id = company, user_id = request.user)
                tran1.save()
                jv_detail1 = VoucherDetail(account_id = account_id, debit = abs(float(value["debit"])), credit = 0.00, header_id = voucher_id, invoice_id = invoice_id)
                jv_detail1.save()
            if value["credit"] > "0" and value["credit"] > "0.00":
                account_id = ChartOfAccount.objects.get(account_title = value["account_title"])
                if check == "1":
                    tran2 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = -abs(float(value["credit"])),
                                        date = datetime.date.today(), remarks = description, account_id = account_id, ref_inv_tran_id = invoice_id, ref_inv_tran_type = 'JV ST', voucher_id = voucher_id.id, company_id = company, user_id = request.user)
                else:
                    tran2 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = -abs(float(value["credit"])),
                                        date = datetime.date.today(), remarks = description, account_id = account_id, ref_inv_tran_id = doc_no, ref_inv_tran_type = 'JV', voucher_id = voucher_id.id, company_id = company, user_id = request.user)
                tran2.save()
                jv_detail2 = VoucherDetail(account_id = account_id,  debit = 0.00, credit = -abs(float(value["credit"])), header_id = voucher_id, invoice_id = invoice_id)
                jv_detail2.save()
        return JsonResponse({"result":"success"})
    return render(request, 'transaction/journal_voucher.html',{"all_invoices":all_invoices,"all_accounts":all_accounts, 'get_last_tran_id':get_last_tran_id,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,
    'allow_report_roles':report_roles(request.user),'permission':permission,'is_superuser':request.user.is_superuser})

@login_required
@user_passes_test(allow_jv_edit)
def edit_journal_voucher(request, pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    jv_header = VoucherHeader.objects.filter(company, id = pk).first()
    jv_detail = VoucherDetail.objects.filter(header_id = jv_header).all()
    account_id = request.POST.get('account_title',False)
    all_accounts = ChartOfAccount.objects.all()
    if account_id:
        account_info = ChartOfAccount.objects.filter(id = account_id).first()
        account_title = account_info.account_title
        account_id = account_info.id
        return JsonResponse({'account_title':account_title, 'account_id':account_id})
    all_invoices = SaleHeader.objects.filter(company).all()
    if request.method == "POST":
        company =  request.session['company']
        company = Company_info.objects.get(id = company)
        company = Q(company_id = company)
        jv_detail.delete()
        ref_inv_tran_type = Q(ref_inv_tran_type = "JV")
        voucher_id = Q(voucher_id = pk)
        Transactions.objects.filter(company, ref_inv_tran_type, voucher_id).all().delete()
        tran_id = request.POST.get('tran_id', False)
        doc_no = request.POST.get('doc_no', False)
        doc_date = request.POST.get('doc_date', False)
        description = request.POST.get('description', False)
        items = json.loads(request.POST.get('items', False))
        date = datetime.date.today()
        jv_header.date = date
        jv_header.doc_no = doc_no
        jv_header.doc_date = doc_date
        jv_header.description = description

        jv_header.save()
        voucher_id = VoucherHeader.objects.get(voucher_no = tran_id)
        company =  request.session['company']
        company = Company_info.objects.get(id = company)
        for value in items:
            header_id = VoucherHeader.objects.get(id = pk)
            account_id = ChartOfAccount.objects.get(account_title = value["account_title"])
            if value["debit"] > "0" and value["debit"] > "0.00":
                tran1 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = "", amount = abs(float(value["debit"])),
                                    date = datetime.date.today(), remarks = description, account_id = account_id, ref_inv_tran_id = doc_no, ref_inv_tran_type = 'JV', voucher_id = voucher_id.id, company_id = company, user_id = request.user)
                tran1.save()
                jv_detail1 = VoucherDetail(account_id = account_id, debit = abs(float(value["debit"])), credit = 0.00, header_id = header_id, invoice_id = 0)
                jv_detail1.save()
            if value["credit"] > "0" and value["credit"] > "0.00":
                print("run")
                print(value["credit"])
                tran2 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = "", amount = -abs(float(value["credit"])),
                                    date = datetime.date.today(), remarks = description, account_id = account_id, ref_inv_tran_id = doc_no, ref_inv_tran_type = 'JV', voucher_id = voucher_id.id, company_id = company, user_id = request.user)
                tran2.save()
                jv_detail2 = VoucherDetail(account_id = account_id,  debit = 0.00, credit = -abs(float(value["credit"])), header_id = header_id, invoice_id = 0)
                jv_detail2.save()
        return JsonResponse({"result":"success"})
    return render(request, 'transaction/edit_journal_voucher.html',{"all_invoices":all_invoices,"all_accounts":all_accounts,'jv_header':jv_header, 'jv_detail':jv_detail,'pk':pk,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})

@login_required
@user_passes_test(allow_jv_delete)
def delete_journal_voucher(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    ref_inv_tran_type = Q(ref_inv_tran_type = "JV ST")
    ref_inv_tran_type2 = Q(ref_inv_tran_type = "JV")
    voucher_id = Q(voucher_id = pk)
    Transactions.objects.filter(company, ref_inv_tran_type, voucher_id|ref_inv_tran_type2).all().delete()
    VoucherDetail.objects.filter(header_id = pk).all().delete()
    VoucherHeader.objects.filter(id = pk).delete()
    messages.add_message(request, messages.SUCCESS, "Journal Voucher Deleted")
    return redirect('journal-voucher-summary')

@login_required
@user_passes_test(allow_crv_print)
def jv_pdf(request, pk):
    company =  request.session['company']
    company_info = Company_info.objects.filter(id = company).all()
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    header = VoucherHeader.objects.filter(company, id = pk).first()
    detail = VoucherDetail.objects.filter(header_id = header.id).all()
    debit = VoucherDetail.objects.filter(header_id = header.id).aggregate(Sum('debit'))
    credit = VoucherDetail.objects.filter(header_id = header.id).aggregate(Sum('credit'))
    pdf = render_to_pdf('transaction/jv_pdf.html', {'company_info':company_info, 'header':header, 'detail':detail, "debit":debit, "credit":credit})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "CashReceivingVoucher.pdf"
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@login_required
@user_passes_test(allow_crv_display)
def view_cash_receiving(request, pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    header_id = VoucherHeader.objects.get(id=pk)
    voucher_header = VoucherHeader.objects.filter(company, id=pk).first()
    voucher_detail = VoucherDetail.objects.filter(header_id=header_id.id).all()
    return render(request, 'transaction/view_cash_receiving_voucher.html', {'voucher_header': voucher_header,'voucher_detail': voucher_detail,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_crv_display)
def cash_receiving_voucher(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = crv_roles(request.user)
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    cursor = connection.cursor()
    all_vouchers = cursor.execute(f'''select * from transaction_voucherheader where voucher_no LIKE '%CRV%' AND company_id_id = {company.id} '''.format(company=company.id))
    all_vouchers = all_vouchers.fetchall()
    return render(request, 'transaction/cash_receiving_voucher.html', {'all_vouchers': all_vouchers,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})



@user_passes_test(allow_crv_add)
@login_required
def new_cash_receiving_voucher(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_inventory_roles = inventory_roles(request.user)
    cursor = connection.cursor()
    get_last_tran_id = cursor.execute('''select * from transaction_voucherheader where voucher_no LIKE '%CRV%' order by voucher_no DESC LIMIT 1  ''')
    get_last_tran_id = get_last_tran_id.fetchall()

    date = datetime.date.today()
    date = date.strftime('%Y%m')
    if get_last_tran_id:
        get_last_tran_id = get_last_tran_id[0][1]
        get_last_tran_id = get_last_tran_id[7:]
        print(get_last_tran_id)
        serial = str((int(get_last_tran_id) + 1))
        get_last_tran_id = date[2:]+'CRV'+serial
    else:
        get_last_tran_id =  date[2:]+'CRV1'
    account_name = request.POST.get('account_title', False)
    check = request.POST.get('check', False)
    invoice_no = request.POST.get('invoice_no', False)
    supplier = Q(account_id = "100")
    customer = Q(account_id = "200")
    all_accounts = ChartOfAccount.objects.filter(supplier|customer).all()
    all_invoices = SaleHeader.objects.filter(payment_method = "Credit", company_id = company.id).all()
    user = request.user
    if account_name:
        if check == "1":
            id = ChartOfAccount.objects.filter(account_title = account_name).first()
            pi = cursor.execute('''Select * From (
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_saledetail
                                Where sale_id_id = HD.ID) + Sum(HD.additional_tax) +
                                ifNull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount
                                ,0 As RcvAmount, HD.sale_no
                                from transaction_saleheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' And HD.account_id_id = %s AND HD.company_id_id = %s AND HD.sale_no = %s AND HD.ID Not In
                                (Select ref_inv_tran_id from transaction_transactions Where ref_inv_tran_type = 'Sale CRV' or ref_inv_tran_type = 'Sale BRV' or ref_inv_tran_type = 'JV ST')
                                Group by HD.ID,HD.account_id_id,account_title
                                Union All
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_saledetail
                                Where sale_id_id = HD.ID) + Sum(HD.additional_tax)
                                + ifnull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount ,
                                (Select Sum(Amount) * -1 From transaction_transactions
                                Where ref_inv_tran_id = HD.ID AND account_id_id = %s) As RcvAmount
                                ,HD.sale_no
                                from transaction_saleheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' AND HD.account_id_id = %s AND HD.sale_no = %s AND HD.company_id_id = %s
                                Group By HD.ID,HD.account_id_id,account_title
                                Having InvAmount > RcvAmount
                                ) As tblPendingInvoice
                                Order By ID
                                ''',[id.id,company.id,invoice_no,id.id,id.id,invoice_no,company.id])
            pi = pi.fetchall()
            return JsonResponse({'pi':pi})
        else:
            id = ChartOfAccount.objects.get(account_title = account_name)
            pi = cursor.execute('''Select * From (
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_saledetail
                                Where sale_id_id = HD.ID) + Sum(HD.additional_tax) +
                                ifNull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount
                                ,0 As RcvAmount, HD.sale_no
                                from transaction_saleheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' And HD.account_id_id = %s AND HD.company_id_id = %s AND HD.ID Not In
                                (Select ref_inv_tran_id from transaction_transactions Where ref_inv_tran_type = 'Sale CRV' or ref_inv_tran_type = 'Sale BRV')
                                Group by HD.ID,HD.account_id_id,account_title
                                Union All
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_saledetail
                                Where sale_id_id = HD.ID) + Sum(HD.additional_tax)
                                + ifnull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount ,
                                (Select Sum(Amount) * -1 From transaction_transactions
                                Where ref_inv_tran_id = HD.ID AND account_id_id = %s) As RcvAmount
                                ,HD.sale_no
                                from transaction_saleheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' AND HD.account_id_id = %s AND HD.company_id_id = %s
                                Group By HD.ID,HD.account_id_id,account_title
                                Having InvAmount > RcvAmount
                                ) As tblPendingInvoice
                                Order By ID
                                ''',[id.id,company.id,id.id,id.id,company.id])
            pi = pi.fetchall()
            return JsonResponse({'pi':pi})
    if request.method == "POST":
        invoice_no = request.POST.get('invoice_no', False)
        doc_date = request.POST.get('doc_date', False)
        description = request.POST.get('description', False)
        customer = request.POST.get('customer', False)
        date = request.POST.get('date', False)
        items = json.loads(request.POST.get('items', False))
        jv_header = VoucherHeader(voucher_no = get_last_tran_id, doc_no = invoice_no, doc_date = doc_date, cheque_no = "-",cheque_date = doc_date, description = description, company_id = company, user_id = request.user)
        jv_header.save()
        voucher_id = VoucherHeader.objects.get(voucher_no = get_last_tran_id)
        for value in items:
            invoice_no = SaleHeader.objects.get(sale_no = value["invoice_no"])

            account_id = ChartOfAccount.objects.get(account_title = customer)
            cash_account = ChartOfAccount.objects.get(account_title = 'Cash')
            amount = float(value["debit"]) - float(value['balance'])

            tran1 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = amount,
                                date = date, remarks = description, account_id = cash_account,ref_inv_tran_id = invoice_no.id,ref_inv_tran_type = "Sale CRV", voucher_id = voucher_id.id, company_id = company,  user_id = request.user)
            tran1.save()
            tran2 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = -abs(amount),
                                date = date, remarks = description, account_id = account_id,ref_inv_tran_id = invoice_no.id,ref_inv_tran_type = "Sale CRV", voucher_id = voucher_id.id, company_id = company,  user_id = request.user)
            tran2.save()
            header_id = VoucherHeader.objects.get(voucher_no = get_last_tran_id)
            jv_detail1 = VoucherDetail(account_id = cash_account, debit = amount, credit = 0.00, header_id = header_id, invoice_id = invoice_no.id)
            jv_detail1.save()
            jv_detail2 = VoucherDetail(account_id = account_id,  debit = 0.00, credit = -abs(amount),header_id = header_id, invoice_id = invoice_no.id)
            jv_detail2.save()
        return JsonResponse({"result":"success"})
    return render(request, 'transaction/new_cash_receiving_voucher.html',{"all_accounts":all_accounts,'all_invoices':all_invoices ,'get_last_tran_id':get_last_tran_id,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_crv_delete)
def delete_cash_receiving(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    ref_inv_tran_type = Q(ref_inv_tran_type = "Sale CRV")
    voucher_id = Q(voucher_id = pk)
    Transactions.objects.filter(company, ref_inv_tran_type, voucher_id).all().delete()
    VoucherDetail.objects.filter(header_id = pk).all().delete()
    VoucherHeader.objects.filter(id = pk).delete()
    messages.add_message(request, messages.SUCCESS, "Cash Receiving Voucher Deleted")
    return redirect('cash-receiving-voucher')


@login_required
@user_passes_test(allow_brv_display)
def view_bank_receiving(request, pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    header_id = VoucherHeader.objects.get(id=pk)
    voucher_header = VoucherHeader.objects.filter(company, id=pk).first()
    voucher_detail = VoucherDetail.objects.filter(header_id=header_id.id).all()
    return render(request, 'transaction/view_bank_receiving_voucher.html', {'voucher_header': voucher_header,'voucher_detail': voucher_detail,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_brv_display)
def bank_receiving_voucher(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    cursor = connection.cursor()
    permission = brv_roles(request.user)
    all_vouchers = cursor.execute('''select * from transaction_voucherheader where voucher_no LIKE '%BRV%' AND company_id_id = {company} '''.format(company=company.id))
    all_vouchers = all_vouchers.fetchall()
    return render(request, 'transaction/bank_receiving_voucher.html', {'all_vouchers': all_vouchers,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_brv_add)
def new_bank_receiving_voucher(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_inventory_roles = inventory_roles(request.user)
    cursor = connection.cursor()
    get_last_tran_id = cursor.execute('''select * from transaction_voucherheader where voucher_no LIKE '%BRV%'
                                        order by voucher_no DESC LIMIT 1''')
    get_last_tran_id = get_last_tran_id.fetchall()

    date = datetime.date.today()
    date = date.strftime('%Y%m')
    if get_last_tran_id:
        get_last_tran_id = get_last_tran_id[0][1]
        get_last_tran_id = get_last_tran_id[7:]
        print(get_last_tran_id)
        serial = str((int(get_last_tran_id) + 1))
        get_last_tran_id = date[2:]+'BRV'+serial
    else:
        get_last_tran_id =  date[2:]+'BRV1'
    account_name = request.POST.get('account_title', False)
    bank_account = request.POST.get('bank_account', False)
    check = request.POST.get('check', False)
    invoice_no = request.POST.get('invoice_no', False)
    customer = Q(account_id = "100")
    supplier = Q(account_id = "200")
    bank = Q(account_id = "300")
    all_accounts = ChartOfAccount.objects.filter(customer|supplier|bank).all()
    banks = Q(parent_id = 16)
    # all_bank = ChartOfAccount.objects.all()
    all_invoices = SaleHeader.objects.filter(company, payment_method = "Credit").all()
    user = request.user
    company =  request.session['company']
    if account_name:
        if check == "1":
            account_id = ChartOfAccount.objects.filter(account_title = bank_account).first()
            id = ChartOfAccount.objects.filter(account_title = account_name).first()
            pi = cursor.execute('''Select * From (
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_saledetail
                                Where sale_id_id = HD.ID) + Sum(HD.additional_tax) +
                                ifNull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount
                                ,0 As RcvAmount, HD.sale_no
                                from transaction_saleheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' And HD.account_id_id = %s AND HD.company_id_id = %s AND HD.sale_no = %s AND HD.ID Not In
                                (Select ref_inv_tran_id from transaction_transactions Where ref_inv_tran_type = 'Sale CRV' or ref_inv_tran_type = 'Sale BRV' or ref_inv_tran_type = 'JV ST')
                                Group by HD.ID,HD.account_id_id,account_title
                                Union All
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_saledetail
                                Where sale_id_id = HD.ID) + Sum(HD.additional_tax)
                                + ifnull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount ,
                                (Select Sum(Amount) * -1 From transaction_transactions
                                Where ref_inv_tran_id = HD.ID AND account_id_id = %s) As RcvAmount
                                ,HD.sale_no
                                from transaction_saleheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' AND HD.account_id_id = %s AND HD.sale_no = %s AND HD.company_id_id = %s
                                Group By HD.ID,HD.account_id_id,account_title
                                Having InvAmount > RcvAmount
                                ) As tblPendingInvoice
                                Order By ID
                                ''',[id.id,company,invoice_no,id.id,id.id,invoice_no,company])
            pi = pi.fetchall()
            return JsonResponse({'pi':pi,'bank_account':bank_account,'account_id':account_id.account_id})
        else:
            id = ChartOfAccount.objects.filter(account_title = account_name).first()
            account_id = ChartOfAccount.objects.filter(account_title = bank_account).first()
            pi = cursor.execute('''Select * From (
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_saledetail
                                Where sale_id_id = HD.ID) + Sum(HD.additional_tax) +
                                ifNull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount
                                ,0 As RcvAmount, HD.sale_no
                                from transaction_saleheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' And HD.account_id_id = %s AND HD.company_id_id = %s AND HD.ID Not In
                                (Select ref_inv_tran_id from transaction_transactions Where ref_inv_tran_type = 'Sale CRV' or ref_inv_tran_type = 'Sale BRV')
                                Group by HD.ID,HD.account_id_id,account_title
                                Union All
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_saledetail
                                Where sale_id_id = HD.ID) + Sum(HD.additional_tax)
                                + ifnull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount ,
                                (Select Sum(Amount) * -1 From transaction_transactions
                                Where ref_inv_tran_id = HD.ID AND account_id_id = %s) As RcvAmount
                                ,HD.sale_no
                                from transaction_saleheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' AND HD.account_id_id = %s AND HD.company_id_id = %s
                                Group By HD.ID,HD.account_id_id,account_title
                                Having InvAmount > RcvAmount
                                ) As tblPendingInvoice
                                Order By ID
                                ''',[id.id,company,id.id,id.id,company])
            pi = pi.fetchall()
            return JsonResponse({'pi':pi,'bank_account':bank_account,'account_id':account_id.account_id})
    if request.method == "POST":
        company =  request.session['company']
        company = Company_info.objects.get(id = company)
        invoice_no = request.POST.get('invoice_no', False)
        doc_date = request.POST.get('doc_date', False)
        cheque_no = request.POST.get('cheque_no', False)
        cheque_date = request.POST.get('cheque_date', False)
        description = request.POST.get('description', False)
        customer = request.POST.get('customer', False)
        bank = request.POST.get('bank', False)
        date = request.POST.get('date', False)
        items = json.loads(request.POST.get('items', False))
        jv_header = VoucherHeader(voucher_no = get_last_tran_id, doc_no = invoice_no, doc_date = doc_date, cheque_no = cheque_no,cheque_date = cheque_date, description = description, company_id = company, user_id = request.user)
        jv_header.save()
        voucher_id = VoucherHeader.objects.get(voucher_no = get_last_tran_id)
        for value in items:
            invoice_no = SaleHeader.objects.get(sale_no = value["invoice_no"])

            account_id = ChartOfAccount.objects.get(account_title = customer)
            bank_account = ChartOfAccount.objects.get(account_title = bank)
            amount = float(value["debit"]) - float(value['balance'])

            tran1 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = amount,
                                date = date, remarks = description, account_id = bank_account,ref_inv_tran_id = invoice_no.id,ref_inv_tran_type = "Sale BRV", voucher_id = voucher_id.id, company_id = company, user_id = request.user )
            tran1.save()
            tran2 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = -abs(amount),
                                date = date, remarks = description, account_id = account_id,ref_inv_tran_id = invoice_no.id,ref_inv_tran_type = "Sale BRV", voucher_id = voucher_id.id, company_id = company, user_id = request.user)
            tran2.save()
            header_id = VoucherHeader.objects.get(voucher_no = get_last_tran_id)
            jv_detail1 = VoucherDetail(account_id = bank_account, debit = amount, credit = 0.00, header_id = header_id, invoice_id = invoice_no.id)
            jv_detail1.save()
            jv_detail2 = VoucherDetail(account_id = account_id,  debit = 0.00, credit = -abs(amount),header_id = header_id, invoice_id = invoice_no.id)
            jv_detail2.save()
        return JsonResponse({"result":"success"})
    return render(request, 'transaction/new_bank_receiving_voucher.html',{"all_accounts":all_accounts, 'get_last_tran_id':get_last_tran_id,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser, 'all_invoices':all_invoices})


@login_required
@user_passes_test(allow_brv_delete)
def delete_bank_receiving(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    ref_inv_tran_type = Q(ref_inv_tran_type = "Sale BRV")
    voucher_id = Q(voucher_id = pk)
    Transactions.objects.filter(company,ref_inv_tran_type, voucher_id).all().delete()
    VoucherDetail.objects.filter(header_id = pk).all().delete()
    VoucherHeader.objects.filter(id = pk).delete()
    messages.add_message(request, messages.SUCCESS, "Cash Receiving Voucher Deleted")
    return redirect('bank-receiving-voucher')


@login_required
@user_passes_test(allow_bpv_display)
def view_bank_payment(request, pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    header_id = VoucherHeader.objects.get(id=pk)
    voucher_header = VoucherHeader.objects.filter(company,id=pk).first()
    voucher_detail = VoucherDetail.objects.filter(header_id=header_id.id).all()
    return render(request, 'transaction/view_bank_payment_voucher.html', {'voucher_header': voucher_header,'voucher_detail': voucher_detail,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_bpv_display)
def bank_payment_voucher(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = bpv_roles(request.user)
    cursor = connection.cursor()
    all_vouchers = cursor.execute('''select * from transaction_voucherheader where voucher_no LIKE '%BPV%' AND company_id_id = {company}'''.format(company=company.id))
    all_vouchers = all_vouchers.fetchall()
    return render(request, 'transaction/bank_payment_voucher.html', {'all_vouchers': all_vouchers,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_bpv_add)
def new_bank_payment_voucher(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_inventory_roles = inventory_roles(request.user)
    cursor = connection.cursor()
    get_last_tran_id = cursor.execute('''select * from transaction_voucherheader where voucher_no LIKE '%BPV%'
                                        order by voucher_no DESC LIMIT 1''')
    get_last_tran_id = get_last_tran_id.fetchall()

    date = datetime.date.today()
    date = date.strftime('%Y%m')
    if get_last_tran_id:
        get_last_tran_id = get_last_tran_id[0][1]
        get_last_tran_id = get_last_tran_id[7:]
        serial = str((int(get_last_tran_id) + 1))
        get_last_tran_id = date[2:]+'BPV'+serial
    else:
        get_last_tran_id =  date[2:]+'BPV1'
    account_name = request.POST.get('account_title', False)
    bank_account = request.POST.get('bank_account', False)
    check = request.POST.get('check', False)
    invoice_no = request.POST.get('invoice_no', False)
    customers = Q(account_id = "100")
    suppliers = Q(account_id = "200")
    bank = Q(account_id = "300")
    all_accounts = ChartOfAccount.objects.filter(customers|suppliers|bank).all()
    banks = Q(parent_id = 16)
    all_bank = ChartOfAccount.objects.filter(customers|suppliers|bank).all()
    all_invoices = PurchaseHeader.objects.filter(company).all()
    user = request.user
    company =  request.session['company']
    if account_name:
        if check == "1":
            account_id = ChartOfAccount.objects.filter(account_title = bank_account).first()
            id = ChartOfAccount.objects.filter(account_title = account_name).first()
            pi = cursor.execute('''Select * From (
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_purchasedetail
                                Where purchase_id_id = HD.ID) + Sum(HD.additional_tax) +
                                ifNull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount
                                ,0 As RcvAmount, HD.purchase_no
                                from transaction_purchaseheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' And HD.account_id_id = %s AND HD.company_id_id = %s AND HD.purchase_no = %s AND HD.ID Not In
                                (Select ref_inv_tran_id from transaction_transactions Where ref_inv_tran_type = 'Purchase BPV')
                                Group by HD.ID,HD.account_id_id,account_title
                                Union All
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_purchasedetail
                                Where purchase_id_id = HD.ID) + Sum(HD.additional_tax)
                                + ifnull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount ,
                                (Select Sum(Amount) * -1 From transaction_transactions
                                Where ref_inv_tran_id = HD.ID AND account_id_id = %s) As RcvAmount
                                ,HD.purchase_no
                                from transaction_purchaseheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' AND HD.account_id_id = %s AND HD.purchase_no = %s AND HD.company_id_id = %s
                                Group By HD.ID,HD.account_id_id,account_title
                                Having InvAmount > RcvAmount
                                ) As tblPendingInvoice
                                Order By ID
                                ''',[id.id,company,invoice_no,id.id,id.id,invoice_no,company])
            pi = pi.fetchall()
            return JsonResponse({'pi':pi,'bank_account':bank_account,'account_id':account_id.account_id})
        else:
            id = ChartOfAccount.objects.get(account_title = account_name)
            account_id = ChartOfAccount.objects.filter(account_title = bank_account).first()
            pi = cursor.execute('''Select * From (
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_purchasedetail
                                Where purchase_id_id = HD.ID) + Sum(HD.additional_tax) +
                                ifNull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount
                                ,0 As RcvAmount, HD.purchase_no
                                from transaction_purchaseheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' And HD.account_id_id = %s AND HD.company_id_id = %s AND HD.ID Not In
                                (Select ref_inv_tran_id from transaction_transactions Where ref_inv_tran_type = 'Purchase CPV' or ref_inv_tran_type = 'Purchase BPV')
                                Group by HD.ID,HD.account_id_id,account_title
                                Union All
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_purchasedetail
                                Where purchase_id_id = HD.ID) + Sum(HD.additional_tax)
                                + ifnull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount ,
                                (Select Sum(Amount) * -1 From transaction_transactions
                                Where ref_inv_tran_id = HD.ID AND account_id_id = %s) As RcvAmount
                                ,HD.purchase_no
                                from transaction_purchaseheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' AND HD.account_id_id = %s AND HD.company_id_id = %s
                                Group By HD.ID,HD.account_id_id,account_title
                                Having InvAmount > RcvAmount
                                ) As tblPendingInvoice
                                Order By ID
                                ''',[id.id,company,id.id,id.id,company])
            pi = pi.fetchall()
            return JsonResponse({'pi':pi,'bank_account':bank_account,'account_id':account_id.account_id})
    if request.method == "POST":
        company =  request.session['company']
        company = Company_info.objects.get(id = company)
        invoice_no = request.POST.get('invoice_no', False)
        doc_date = request.POST.get('doc_date', False)
        cheque_no = request.POST.get('cheque_no', False)
        cheque_date = request.POST.get('cheque_date', False)
        description = request.POST.get('description', False)
        customer = request.POST.get('customer', False)
        bank = request.POST.get('bank', False)
        date = request.POST.get('date', False)
        items = json.loads(request.POST.get('items', False))
        jv_header = VoucherHeader(voucher_no = get_last_tran_id, doc_no = invoice_no, doc_date = doc_date, cheque_no = cheque_no,cheque_date = cheque_date, description = description, company_id = company, user_id = request.user)
        jv_header.save()
        voucher_id = VoucherHeader.objects.get(voucher_no = get_last_tran_id)
        for value in items:
            invoice_no = PurchaseHeader.objects.get(purchase_no = value["invoice_no"])

            account_id = ChartOfAccount.objects.get(account_title = customer)
            bank_account = ChartOfAccount.objects.get(account_title = bank)
            amount = float(value["credit"]) - float(value['balance'])

            tran1 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = -abs(amount),
                                date = date, remarks = description, account_id = bank_account,ref_inv_tran_id = invoice_no.id,ref_inv_tran_type = "Purchase BPV", voucher_id = voucher_id.id , company_id = company, user_id = request.user )
            tran1.save()
            tran2 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = amount,
                                date = date, remarks = description, account_id = account_id,ref_inv_tran_id = invoice_no.id,ref_inv_tran_type = "Purchase BPV", voucher_id = voucher_id.id , company_id = company, user_id = request.user)
            tran2.save()
            header_id = VoucherHeader.objects.get(voucher_no = get_last_tran_id)
            jv_detail1 = VoucherDetail(account_id = bank_account, debit = 0.00, credit = -abs(amount), header_id = header_id, invoice_id = invoice_no.id)
            jv_detail1.save()
            jv_detail2 = VoucherDetail(account_id = account_id,  debit = amount, credit = 0.00,header_id = header_id, invoice_id = invoice_no.id)
            jv_detail2.save()
        return JsonResponse({"result":"success"})
    return render(request, 'transaction/new_bank_payment_voucher.html',{"all_accounts":all_accounts, 'get_last_tran_id':get_last_tran_id,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser,'all_bank':all_bank,'all_invoices':all_invoices})



@login_required
@user_passes_test(allow_bpv_delete)
def delete_bank_payment(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    ref_inv_tran_type = Q(ref_inv_tran_type = "Purchase BPV")
    voucher_id = Q(voucher_id = pk)
    Transactions.objects.filter(company, ref_inv_tran_type, voucher_id).all().delete()
    VoucherDetail.objects.filter(header_id = pk).all().delete()
    VoucherHeader.objects.filter(company, id = pk).delete()
    messages.add_message(request, messages.SUCCESS, "Bank Payment Voucher Deleted")
    return redirect('bank-payment-voucher')


@login_required
@user_passes_test(allow_cpv_display)
def view_cash_payment(request, pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    header_id = VoucherHeader.objects.get(id=pk)
    voucher_header = VoucherHeader.objects.filter(company, id=pk).first()
    voucher_detail = VoucherDetail.objects.filter(header_id=header_id.id).all()
    return render(request, 'transaction/view_cash_receiving_voucher.html', {'voucher_header': voucher_header,'voucher_detail': voucher_detail,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_cpv_display)
def cash_payment_voucher(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    permission = cpv_roles(request.user)
    cursor = connection.cursor()
    all_vouchers = cursor.execute('''select * from transaction_voucherheader where voucher_no LIKE '%CPV%' AND company_id_id = {company}'''.format(company=company.id))
    all_vouchers = all_vouchers.fetchall()
    return render(request, 'transaction/cash_payment_voucher.html', {'all_vouchers': all_vouchers,'permission':permission,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_cpv_add)
def new_cash_payment_voucher(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    cursor = connection.cursor()
    get_last_tran_id = cursor.execute('''select * from transaction_voucherheader where voucher_no LIKE '%CPV%'
                                        order by voucher_no DESC LIMIT 1''')
    get_last_tran_id = get_last_tran_id.fetchall()

    date = datetime.date.today()
    date = date.strftime('%Y%m')
    if get_last_tran_id:
        get_last_tran_id = get_last_tran_id[0][1]
        get_last_tran_id = get_last_tran_id[7:]
        print(get_last_tran_id)
        serial = str((int(get_last_tran_id) + 1))
        get_last_tran_id = date[2:]+'CPV'+serial
    else:
        get_last_tran_id =  date[2:]+'CPV1'
    account_name = request.POST.get('account_title', False)
    check = request.POST.get('check', False)
    invoice_no = request.POST.get('invoice_no', False)
    customers = Q(account_id = "100")
    suppliers = Q(account_id = "200")
    bank = Q(account_id = "300")
    all_accounts = ChartOfAccount.objects.filter(customers|suppliers|bank).all()
    all_invoices = PurchaseHeader.objects.filter(company).all()
    user = request.user
    company =  request.session['company']
    if account_name:
        if check == "1":
            id = ChartOfAccount.objects.filter(account_title = account_name).first()
            pi = cursor.execute('''Select * From (
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_purchasedetail
                                Where purchase_id_id = HD.ID) + Sum(HD.additional_tax) +
                                ifNull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount
                                ,0 As RcvAmount, HD.purchase_no
                                from transaction_purchaseheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' And HD.account_id_id = %s AND HD.company_id_id = %s AND HD.purchase_no = %s AND HD.ID Not In
                                (Select ref_inv_tran_id from transaction_transactions Where ref_inv_tran_type = 'Purchase CPV' or ref_inv_tran_type = 'Purchase BPV')
                                Group by HD.ID,HD.account_id_id,account_title
                                Union All
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_purchasedetail
                                Where purchase_id_id = HD.ID) + Sum(HD.additional_tax)
                                + ifnull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount ,
                                (Select Sum(Amount) * -1 From transaction_transactions
                                Where ref_inv_tran_id = HD.ID AND account_id_id = %s) As RcvAmount
                                ,HD.purchase_no
                                from transaction_purchaseheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' AND HD.account_id_id = %s AND HD.purchase_no = %s AND HD.company_id_id = %s
                                Group By HD.ID,HD.account_id_id,account_title
                                Having InvAmount > RcvAmount
                                ) As tblPendingInvoice
                                Order By ID
                                ''',[id.id,company,invoice_no,id.id,id.id,invoice_no,company])
            pi = pi.fetchall()
            return JsonResponse({'pi':pi})
        else:
            id = ChartOfAccount.objects.get(account_title = account_name)
            pi = cursor.execute('''Select * From (
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_purchasedetail
                                Where purchase_id_id = HD.ID) + Sum(HD.additional_tax) +
                                ifNull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount
                                ,0 As RcvAmount, HD.purchase_no
                                from transaction_purchaseheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' And HD.account_id_id = %s AND HD.company_id_id = %s AND HD.ID Not In
                                (Select ref_inv_tran_id from transaction_transactions Where ref_inv_tran_type = 'Purchase CPV' or ref_inv_tran_type = 'Purchase BPV')
                                Group by HD.ID,HD.account_id_id,account_title
                                Union All
                                Select HD.ID,HD.account_id_id,account_title,
                                ((Select Sum(total) From transaction_purchasedetail
                                Where purchase_id_id = HD.ID) + Sum(HD.additional_tax)
                                + ifnull((Select Sum(cartage) From transaction_cartage_and_po
                                Where invoice_id = HD.ID),0)) As InvAmount ,
                                (Select Sum(Amount) * -1 From transaction_transactions
                                Where ref_inv_tran_id = HD.ID AND account_id_id = %s) As RcvAmount
                                ,HD.purchase_no
                                from transaction_purchaseheader HD
                                Inner Join transaction_chartofaccount COA on HD.account_id_id = COA.id
                                Where Payment_method = 'Credit' AND HD.account_id_id = %s AND HD.company_id_id = %s
                                Group By HD.ID,HD.account_id_id,account_title
                                Having InvAmount > RcvAmount
                                ) As tblPendingInvoice
                                Order By ID
                                ''',[id.id,company,id.id,id.id,company])
            pi = pi.fetchall()
            return JsonResponse({'pi':pi})
    company = Company_info.objects.get(id = company)
    if request.method == "POST":
        invoice_no = request.POST.get('invoice_no', False)
        doc_date = request.POST.get('doc_date', False)
        description = request.POST.get('description', False)
        customer = request.POST.get('customer', False)
        date = request.POST.get('date', False)
        items = json.loads(request.POST.get('items', False))
        jv_header = VoucherHeader(voucher_no = get_last_tran_id, doc_no = invoice_no, doc_date = doc_date, cheque_no = "-",cheque_date = doc_date, description = description , company_id = company, user_id = request.user)
        jv_header.save()
        voucher_id = VoucherHeader.objects.get(voucher_no = get_last_tran_id)
        for value in items:
            invoice_no = PurchaseHeader.objects.get(purchase_no = value["invoice_no"])

            account_id = ChartOfAccount.objects.get(account_title = customer)
            cash_account = ChartOfAccount.objects.get(account_title = 'Cash')
            amount = float(value["credit"]) - float(value['balance'])

            tran1 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = -abs(amount),
                                date = date, remarks = description, account_id = cash_account,ref_inv_tran_id = invoice_no.id,ref_inv_tran_type = "Purchase CPV", voucher_id = voucher_id.id )
            tran1.save()
            tran2 = Transactions(refrence_id = 0, refrence_date = doc_date, tran_type = '', amount = amount,
                                date = date, remarks = description, account_id = account_id,ref_inv_tran_id = invoice_no.id,ref_inv_tran_type = "Purchase CPV", voucher_id = voucher_id.id )
            tran2.save()
            header_id = VoucherHeader.objects.get(voucher_no = get_last_tran_id)
            jv_detail1 = VoucherDetail(account_id = cash_account, debit = 0.00, credit = -abs(amount), header_id = header_id, invoice_id = invoice_no.id)
            jv_detail1.save()
            jv_detail2 = VoucherDetail(account_id = account_id,  debit = amount, credit = 0.00,header_id = header_id, invoice_id = invoice_no.id)
            jv_detail2.save()
        return JsonResponse({"result":"success"})
    return render(request, 'transaction/new_cash_payment_voucher.html',{"all_accounts":all_accounts, 'get_last_tran_id':get_last_tran_id,'all_invoices':all_invoices,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(allow_cpv_delete)
def delete_cash_payment(request,pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    ref_inv_tran_type = Q(ref_inv_tran_type = "Purchase CPV")
    voucher_id = Q(voucher_id = pk)
    Transactions.objects.filter(company, ref_inv_tran_type, voucher_id).all().delete()
    VoucherDetail.objects.filter(header_id = pk).all().delete()
    VoucherHeader.objects.filter(company,id = pk).delete()
    messages.add_message(request, messages.SUCCESS, "Cash Payment Voucher Deleted")
    return redirect('cash-payment-voucher')

@login_required
@user_passes_test(allow_crv_print)
def crv_pdf(request, pk):
    company =  request.session['company']
    company_info = Company_info.objects.filter(id = company).all()
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    header = VoucherHeader.objects.filter(company, id = pk).first()
    details = VoucherDetail.objects.filter(debit = 0,header_id = header.id).first()
    cursor = connection.cursor()
    detail = cursor.execute('''select sum(VD.credit) as Amount,COA.account_title, COA.account_id
                            from transaction_voucherdetail VD
                            inner join transaction_voucherheader VH on VH.id = VD.header_id_id
                            inner join transaction_chartofaccount COA on VD.account_id_id = COA.id
                            where VD.header_id_id = %s AND VD.account_id_id = %s
                            ''',[header.id,details.account_id.id])
    detail = detail.fetchall()
    amount_in_words =  num2words(abs(detail[0][0]))
    pdf = render_to_pdf('transaction/crv_pdf.html', {'company_info':company_info, 'header':header, 'detail':detail, 'amount_in_words':amount_in_words})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "CashReceivingVoucher.pdf"
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

@login_required
@user_passes_test(allow_cpv_print)
def cpv_pdf(request, pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company_info = Company_info.objects.filter(id = company.id).all()
    company = Q(company_id = company)
    header = VoucherHeader.objects.filter(company, id = pk).first()
    details = VoucherDetail.objects.filter(credit = 0,header_id = header.id).first()
    cursor = connection.cursor()
    detail = cursor.execute('''select sum(VD.debit) as Amount,COA.account_title, COA.account_id
                            from transaction_voucherdetail VD
                            inner join transaction_voucherheader VH on VH.id = VD.header_id_id
                            inner join transaction_chartofaccount COA on VD.account_id_id = COA.id
                            where VD.header_id_id = %s AND VD.account_id_id = %s
                            ''',[header.id,details.account_id.id])
    detail = detail.fetchall()
    amount_in_words =  num2words(abs(detail[0][0]))
    pdf = render_to_pdf('transaction/cpv_pdf.html', {'company_info':company_info, 'header':header, 'detail':detail, 'amount_in_words':amount_in_words})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "CashReceivingVoucher.pdf"
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@login_required
@user_passes_test(allow_bpv_print)
def bpv_pdf(request, pk):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company_info = Company_info.objects.filter(id=company.id).all()
    company = Q(company_id = company)
    header = VoucherHeader.objects.filter(company, id = pk).first()
    details = VoucherDetail.objects.filter(credit = 0,header_id = header.id).first()
    cursor = connection.cursor()
    detail = cursor.execute('''select sum(VD.debit) as Amount,COA.account_title, COA.account_id
                            from transaction_voucherdetail VD
                            inner join transaction_voucherheader VH on VH.id = VD.header_id_id
                            inner join transaction_chartofaccount COA on VD.account_id_id = COA.id
                            where VD.header_id_id = %s AND VD.account_id_id = %s
                            ''',[header.id,details.account_id.id])
    detail = detail.fetchall()
    amount_in_words =  num2words(abs(detail[0][0]))
    bank = VoucherDetail.objects.filter(debit = 0, header_id = pk).first()
    pdf = render_to_pdf('transaction/bpv_pdf.html', {'company_info':company_info, 'header':header, 'detail':detail, 'amount_in_words':amount_in_words,'bank':bank})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "CashReceivingVoucher.pdf"
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@login_required
@user_passes_test(allow_brv_print)
def brv_pdf(request, pk):
    company =  request.session['company']
    company_info = Company_info.objects.filter(id = company).all()
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    header = VoucherHeader.objects.filter(company,id = pk).first()
    details = VoucherDetail.objects.filter(debit = 0,header_id = header.id).first()
    cursor = connection.cursor()
    print(details.account_id.id)
    detail = cursor.execute('''select sum(VD.credit) as Amount,COA.account_title, COA.account_id
                            from transaction_voucherdetail VD
                            inner join transaction_voucherheader VH on VH.id = VD.header_id_id
                            inner join transaction_chartofaccount COA on VD.account_id_id = COA.id
                            where VD.header_id_id = %s AND VD.account_id_id = %s
                            ''',[header.id,details.account_id.id])
    detail = detail.fetchall()
    print(detail)
    amount_in_words =  num2words(abs(detail[0][0]))
    bank = VoucherDetail.objects.filter(credit = 0, header_id = pk).first()
    pdf = render_to_pdf('transaction/brv_pdf.html', {'company_info':company_info, 'header':header, 'detail':detail, 'amount_in_words':amount_in_words,'bank':bank})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "CashReceivingVoucher.pdf"
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@login_required
def account_ledger(request):
    company =  request.session['company']
    if request.method == "POST":
        debit_amount = 0
        credit_amount = 0
        pk = request.POST.get('account_title')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        company_info = Company_info.objects.filter(id=company).all()
        image = Company_info.objects.filter(id=1).first()
        cursor = connection.cursor()
        cursor.execute('''Select tran_type,refrence_id,refrence_date,remarks,ref_inv_tran_id,ref_inv_tran_type,Sum(Debit) Debit,Sum(Credit) Credit From (
                    Select Distinct account_id_id,'Opening' As tran_type,'' As refrence_id,'' As refrence_date,'Opening Balance' As remarks,
                    '' AS ref_inv_tran_id,'' AS ref_inv_tran_type,
                    Case When Sum(amount) > -1 Then  sum(amount) Else 0 End As Debit,
                    Case When Sum(amount) < -1 Then  sum(amount) Else 0 End As Credit from (
                    Select id As Account_id_id, Sum(Opening_Balance) As amount
                    From transaction_chartofaccount Where ID = (
                    Select id from transaction_chartofaccount Where Parent_ID = %s)
                    Union All
                    Select id As account_id_id, Sum(Opening_Balance) As amount
                    From transaction_chartofaccount Where ID = (%s)
                    Union All
                    Select account_id_id,Sum(amount) As amount From transaction_transactions
                    where account_id_id in (
                    Case When (Select id from transaction_chartofaccount Where Parent_ID = %s)
                    <> '' Then (Select id from transaction_chartofaccount Where Parent_ID = %s)
                    Else (%s) END) AND refrence_date < %s
                    Union all
                    Select account_id_id,Sum(amount) As amount From transaction_transactions
                    where account_id_id in (%s) AND refrence_date < %s
                    ) tblData
                    Group By account_id_id
                    Union all
                    Select Distinct account_id_id,tran_type,refrence_id,refrence_date,remarks,ref_inv_tran_id,ref_inv_tran_type,
                    Case When amount > -1 Then  amount Else 0 End As Debit,
                    Case When amount < -1 Then  amount Else 0 End As Credit from (
                    Select * From transaction_transactions
                    where account_id_id in (
                    Case When (Select id from transaction_chartofaccount Where Parent_ID = %s)
                    <> '' Then (Select id from transaction_chartofaccount Where Parent_ID = %s)
                    Else (%s) END)
                    Union all
                    Select * From transaction_transactions
                    where account_id_id in (%s)
                    ) tblData
                    Where refrence_date Between %s And %s
                    Order By account_id_id,refrence_date Asc
                    ) As tblLedger
                    Group By tran_type,refrence_id,refrence_date,remarks,ref_inv_tran_id,ref_inv_tran_type
                    Order By refrence_date Asc
                    ''',[pk,pk,pk,pk,pk,from_date,pk,from_date,pk,pk,pk,pk,from_date,to_date])
        row = cursor.fetchall()
        print(row)
        ledger_list = []
        balance = 0
        for i,value in enumerate(row):
            balance = balance + float(value[6]) + float(value[7])
            info = {
            "date": value[2],
            "voucher_no": value[3],
            "tran_type": value[0],
            "debit":value[6],
            "credit":value[7],
            "balance": balance,
            }
            ledger_list.append(info)
        if row:
            for v in row:
                if v[6] >= 0:
                    debit_amount = debit_amount + v[6]
                if v[7] <= 0:
                    credit_amount = credit_amount + v[7]
        account_id = ChartOfAccount.objects.filter(id = pk).first()
        account_title = account_id.account_title
        id = account_id.id
        pdf = render_to_pdf('transaction/account_ledger_pdf.html', {'ledger_list':ledger_list,'company_info':company_info,'image':image,'row':row, 'debit_amount':debit_amount, 'credit_amount': credit_amount, 'account_title':account_title, 'from_date':from_date,'to_date':to_date,'id':id})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "TrialBalance%s.pdf" %("000")
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('report')

@login_required
def trial_balance(request):
    company =  request.session['company']
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    if request.method == "POST":
        debit_amount = 0
        credit_amount = 0
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        company_info = Company_info.objects.filter(id=company).all()
        cursor = connection.cursor()
        cursor.execute('''Select id,account_title,ifnull(amount,0) + opening_balance As Amount
                        from transaction_chartofaccount
                        Left Join
                        (select account_id_id,sum(AMount) As Amount from transaction_transactions
                        Where transaction_transactions.date Between %s And %s
                        Group By account_id_id) As tbltran On transaction_chartofaccount.id = tbltran.account_id_id
                        ''',[from_date, to_date])
        row = cursor.fetchall()
        for v in row:
            if v[2] >= 0:
                debit_amount = debit_amount + v[2]
            else:
                credit_amount = credit_amount + v[2]
        pdf = render_to_pdf('transaction/trial_balance_pdf.html', {'company_info':company_info,'row':row, 'debit_amount':debit_amount, 'credit_amount': credit_amount,'from_date':from_date,'to_date':to_date,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "TrialBalance%s.pdf" %("000")
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('report')


@login_required
def sale_detail(request):
    company =  request.session['company']
    company = Company_info.objects.get(id = company)
    company = Q(company_id = company)
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    if request.method == "POST":
        debit_amount = 0
        credit_amount = 0
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        company_info = Company_info.objects.all()
        image = Company_info.objects.filter(company_name = "Hamza Enterprise").first()
        cursor = connection.cursor()
        cursor.execute('''Select id,account_title,ifnull(amount,0) + opening_balance As Amount
                        from transaction_chartofaccount
                        Left Join
                        (select account_id_id,sum(AMount) As Amount from transaction_transactions
                        Where transaction_transactions.date Between %s And %s
                        Group By account_id_id) As tbltran On transaction_chartofaccount.id = tbltran.account_id_id
                        ''',[from_date, to_date])
        row = cursor.fetchall()
        for v in row:
            if v[2] >= 0:
                debit_amount = debit_amount + v[2]
            else:
                credit_amount = credit_amount + v[2]
        pdf = render_to_pdf('transaction/trial_balance_pdf.html', {'company_info':company_info,'image':image,'row':row, 'debit_amount':debit_amount, 'credit_amount': credit_amount,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "TrialBalance%s.pdf" %("000")
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('report')

@login_required
def sale_detail_item_wise(request):
    company =  request.session['company']
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    total = 0
    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        company_info = Company_info.objects.filter(id=company)
        print(company_info)
        cursor = connection.cursor()
        cursor.execute('''Select item_code, item_name, item_description,Sum(Total) As TotalAmount From (
                    select IP.product_code as item_code , IP.product_name as item_name, IP.product_desc as item_description, sum(SD.cost_price * SD.quantity) As Total
                    from transaction_saleheader SH
                    inner join inventory_add_products IP on IP.id = SD.item_id_id
                    inner join transaction_saledetail SD
                    on SD.sale_id_id = SH.id
                    where SH.date Between %s And %s
                    Group by item_code
                    Union All
                    select IP.product_code as item_code, IP.product_name as item_name, IP.product_desc as item_description, sum(SRD.cost_price * SRD.quantity) As Total
                    from transaction_salereturnheader SRH
                    inner join inventory_add_products IP on IP.id = SRD.item_id_id
                    inner join transaction_salereturndetail SRD
                    on SRD.sale_return_id_id = SRH.id
                    where SRH.date Between %s And %s
                    Group by item_code
                    ) tblData
                    group by item_code
                    ''',[from_date, to_date,from_date, to_date])
        row = cursor.fetchall()
        for value in row:
            total = total + value[3]
        print(total)
        pdf = render_to_pdf('transaction/sale_detail_item_wise_pdf.html', {'company_info':company_info,'row':row,'from_date':from_date, 'to_date':to_date,'total':total,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Sale_Detail_Item_Wise%s.pdf" %("000")
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('report')


@login_required
def sale_summary_item_wise(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    total = 0
    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        account_id = request.POST.get('account_id')
        print(account_id)
        company_info = Company_info.objects.filter(id = 1).first()
        print(company_info)
        # image = Company_info.objects.filter(company_name = "Hamza Enterprise").first()
        all_accounts = ChartOfAccount.objects.all()
        cursor = connection.cursor()
        cursor.execute('''Select item_code, item_name, item_description,Sum(Total) As TotalAmount From (
                            select IP.product_code as item_code , IP.product_name as item_name, IP.product_desc as item_description, sum(SD.cost_price * SD.quantity) As Total
                            from transaction_saleheader SH
                            inner join inventory_add_products IP on IP.id = SD.item_id_id
                            inner join transaction_saledetail SD
                            on SD.sale_id_id = SH.id
                            where SH.date Between %s And %s
                            Group by item_code
                            Union All
                            select IP.product_code as item_code, IP.product_name as item_name, IP.product_desc as item_description, sum(SRD.cost_price * SRD.quantity) As Total
                            from transaction_salereturnheader SRH
                            inner join inventory_add_products IP on IP.id = SRD.item_id_id
                            inner join transaction_salereturndetail SRD
                            on SRD.sale_return_id_id = SRH.id
                            where SRH.date Between %s And %s
                            Group by item_code
                            ) tblData
                            group by item_code
                             ''',[from_date, to_date,from_date, to_date, account_id])
        row = cursor.fetchall()
        for value in row:
            total = total + value[5]
        account_id = ChartOfAccount.objects.filter(id = account_id).first()
        account_title = account_id.account_title
        pdf = render_to_pdf('transaction/sale_summary_item_wise_pdf.html', {'company_info':company_info,'image':image,'row':row,'from_date':from_date, 'to_date':to_date,'total':total, 'all_accounts':all_accounts, 'account_title':account_title,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Sale_Detail_Item_Wise%s.pdf" %("000")
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return redirect('report')


@login_required
def sales_tax_invoice(request,pk):
    company = request.session["company"]
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    cursor = connection.cursor()
    lines = 0
    total_amount_item = 0
    tax_amount = 0
    ca = 0
    company_info = Company_info.objects.filter(id=company)
    header = SaleHeader.objects.filter(id = pk).first()
    detail = cursor.execute('''Select SaleId,DcNo,po_no,product_name, product_desc, unit, quantity, cost_price, sales_tax, total from(
                            select SD.sale_id_id as SaleID, PS.id,PS.product_name as product_name, PS.product_desc as product_desc, PS.unit as unit,
                            SD.quantity as quantity, SD.cost_price as cost_price, SD.sales_tax as sales_tax,
                            DC.dc_no as DcNo, DCD.PO_no  as po_no, total
                            from transaction_saledetail SD
                            inner join inventory_add_products PS on PS.id = SD.item_id_id
                            inner join customer_dcheadercustomer DC on SD.dc_ref = DC.id
                            inner join customer_dcdetailcustomer DCD on DCD.dc_id_id = DC.id
                            left join customer_poheadercustomer PO on PO.id = DCD.po_no
                            group by SD.id
                            )as tblData where tblData.SaleId =  %s ''',[pk])
    detail = detail.fetchall()
    hs_code = SaleDetail.objects.filter(sale_id = pk).first()
    if header.account_id.parent_id == 13 or header.account_id.parent_id == 12:
        parent_company_name = header.account_id
    else:
        parent_company_name = ChartOfAccount.objects.filter(id = header.account_id.parent_id).first()
    print(parent_company_name)
    for value in detail:
        lines = lines + len(value[4].split('\n'))
        amount = float(value[7] * value[6])
        total_amount_item = total_amount_item + amount
        sales_tax_amount = amount * 17 / 100
        tax_amount = tax_amount + sales_tax_amount
        tax_amount = tax_amount
        total_amount_item = total_amount_item + sales_tax_amount
        total_amount_item = total_amount_item
    total_amount_item = round(total_amount_item)
    total_amount = total_amount_item
    total_amount = round(total_amount)
    lines = lines + len(detail) + len(detail)
    total_lines = 36 - lines
    pdf = render_to_pdf('transaction/sales_tax_invoice_pdf_lines.html', {'company_info':company_info,'header':header, 'detail':detail,'total_lines':total_lines,'total_amount_item':total_amount_item,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,'is_superuser':request.user.is_superuser, 'parent_company_name':parent_company_name,'tax_amount':tax_amount,'total_amount':total_amount,'hs_code':hs_code,'allow_report_roles':report_roles(request.user)})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "SaleTaxInvoice%s.pdf" %(header.sale_no)
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

@login_required
def commercial_invoice(request,pk):
    company = request.session["company"]
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    cursor = connection.cursor()
    lines = 0
    total_amount_item = 0
    tax_amount = 0
    cartage = 0
    company_info = Company_info.objects.filter(id=company)
    header = SaleHeader.objects.filter(id = pk).first()
    detail = cursor.execute('''Select SaleId,DcNo,po_no,product_name, product_desc, unit, quantity, cost_price, sales_tax, total from(
                            select SD.sale_id_id as SaleID, PS.id,PS.product_name as product_name, PS.product_desc as product_desc, PS.unit as unit,
                            SD.quantity as quantity, SD.cost_price as cost_price, SD.sales_tax as sales_tax,
                            DC.dc_no as DcNo, DCD.PO_no  as po_no, total
                            from transaction_saledetail SD
                            inner join inventory_add_products PS on PS.id = SD.item_id_id
                            inner join customer_dcheadercustomer DC on SD.dc_ref = DC.id
                            inner join customer_dcdetailcustomer DCD on DCD.dc_id_id = DC.id
                            left join customer_poheadercustomer PO on PO.id = DCD.po_no
                            group by SD.id
                            )as tblData where tblData.SaleId = %s ''',[pk])
    detail = detail.fetchall()
    hs_code = SaleDetail.objects.filter(sale_id = pk).first()
    if header.account_id.parent_id == 13 or header.account_id.parent_id == 12:
        parent_company_name = header.account_id
    else:
        parent_company_name = ChartOfAccount.objects.filter(id = header.account_id.parent_id).first()
    cartage_amounts = Cartage_and_Po.objects.filter(invoice_id = pk).all()
    for value in cartage_amounts:
        cartage = cartage + value.cartage
    for value in detail:
        lines = lines + len(value[4].split('\n'))
        amount = float(value[7] * value[6])
        total_amount_item = total_amount_item + amount
        sales_tax_amount = amount * 17 / 100
        tax_amount = tax_amount + sales_tax_amount
        tax_amount = tax_amount
        total_amount_item = total_amount_item + sales_tax_amount
        total_amount_item = total_amount_item
    total_amount_item = round(total_amount_item)
    tax_amount = round(tax_amount)
    total_amount = Decimal(total_amount_item) + Decimal(cartage) + Decimal(header.additional_tax)
    total_amount = round(total_amount)
    lines = lines + len(detail) + len(detail)
    total_lines = 36 - lines
    pdf = render_to_pdf('transaction/commercial_invoice_pdf_lines.html', {'company_info':company_info,'header':header, 'detail':detail,'total_lines':total_lines,'total_amount_item':total_amount_item,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,'is_superuser':request.user.is_superuser, 'parent_company_name':parent_company_name, 'cartage_amounts':cartage_amounts,'tax_amount':tax_amount,'total_amount':total_amount,'hs_code':hs_code,'allow_report_roles':report_roles(request.user)})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "SaleTaxInvoice%s.pdf" %(header.sale_no)
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@login_required
def commercial_invoice_non_gst(request,pk):
    company = request.session["company"]
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    cursor = connection.cursor()
    lines = 0
    total_amount_item = 0
    tax_amount = 0
    cartage = 0
    company_info = Company_info.objects.filter(id=company)
    header = SaleHeader.objects.filter(id = pk).first()
    detail = cursor.execute('''Select SaleId,DcNo,po_no,product_name, product_desc, unit, quantity, cost_price, sales_tax from(
                            select SD.sale_id_id as SaleID, PS.id,PS.product_name as product_name, PS.product_desc as product_desc, PS.unit as unit,
                            SD.quantity as quantity, SD.cost_price as cost_price, SD.sales_tax as sales_tax,
                            DC.dc_no as DcNo, DCD.PO_no  as po_no
                            from transaction_saledetail SD
                            inner join inventory_add_products PS on PS.id = SD.item_id_id
                            inner join customer_dcheadercustomer DC on SD.dc_ref = DC.id
                            inner join customer_dcdetailcustomer DCD on DCD.dc_id_id = DC.id
                            left join customer_poheadercustomer PO on PO.id = DCD.po_no
                            group by SD.id
                            )as tblData where tblData.SaleId = %s ''',[pk])
    detail = detail.fetchall()
    hs_code = SaleDetail.objects.filter(sale_id = pk).first()
    if header.account_id.parent_id == 5 or header.account_id.parent_id == 13:
        parent_company_name = header.account_id
    else:
        parent_company_name = ChartOfAccount.objects.filter(id = header.account_id.parent_id).first()
    print(parent_company_name)
    cartage_amounts = Cartage_and_Po.objects.filter(invoice_id = pk).all()
    for value in cartage_amounts:
        cartage = cartage + value.cartage
    for value in detail:
        lines = lines + len(value[4].split('\n'))
        amount = float(value[7] * value[6])
        total_amount_item = total_amount_item + amount
        total_amount_item = round(total_amount_item)
    total_amount = total_amount_item + cartage
    total_amount = round(total_amount)
    lines = lines + len(detail) + len(detail)
    total_lines = 36 - lines
    pdf = render_to_pdf('transaction/commercial_invoice_pdf_non_gst.html', {'company_info':company_info,'header':header, 'detail':detail,'total_lines':total_lines,'total_amount_item':total_amount_item,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,'is_superuser':request.user.is_superuser, 'parent_company_name':parent_company_name, 'cartage_amounts':cartage_amounts,'total_amount':total_amount,'allow_report_roles':report_roles(request.user)})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "SaleTaxInvoice%s.pdf" %(header.sale_no)
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@login_required
@user_passes_test(Is_superuser)
def multi_companies(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    all_companies = Company_info.objects.all()
    return render(request,'transaction/multi_companies.html',{'all_companies':all_companies,'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(Is_superuser)
def new_multi_companies(request):
    allow_customer_roles = customer_roles(request.user)
    allow_supplier_roles = supplier_roles(request.user)
    allow_transaction_roles = transaction_roles(request.user)
    allow_inventory_roles = inventory_roles(request.user)
    all_companies = Company_info.objects.all()
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        company_type = request.POST.get('company_type')
        phone_no = request.POST.get('phone_no')
        mobile_no = request.POST.get('mobile_no')
        email_address = request.POST.get('email_address')
        web_site = request.POST.get('web_site')
        ntn = request.POST.get('ntn')
        stn = request.POST.get('stn')
        cnic = request.POST.get('cnic')
        new_companies = Company_info(company_name = company_name, company_address = company_address, company_type = company_type ,phone_no = phone_no, email = email_address,  website = web_site, ntn = ntn, stn = stn, cnic = cnic)
        new_companies.save()
    return render(request,'transaction/new_multi_company.html',{'allow_customer_roles':allow_customer_roles,'allow_supplier_roles':allow_supplier_roles,'allow_transaction_roles':allow_transaction_roles,'allow_inventory_roles':allow_inventory_roles,    'allow_report_roles':report_roles(request.user),'is_superuser':request.user.is_superuser})


@login_required
@user_passes_test(Is_superuser)
def edit_multi_companies(request,pk):
    company = Company_info.objects.get(id= pk)
    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST,instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, f'Company Profile has been updated!')
            return redirect('multi-companies')
    else:
        form = CompanyUpdateForm(instance=company)

    return render(request,'transaction/edit_multi_company.html',{'form':form})


@login_required
@user_passes_test(Is_superuser)
def delete_multi_companies(request,pk):
    Company_info.objects.filter(id= pk).all().delete()
    messages.add_message(request, messages.SUCCESS, "Company Deleted.")
    return redirect('multi-companies')
