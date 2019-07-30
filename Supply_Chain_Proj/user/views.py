from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationFrom
from  supplier.models import Company_info
from .models import UserRoles
from django.db.models import Q
from supplier.views import quotation_roles

def register(request):
    allow_quotation_roles = quotation_roles()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = RegistrationFrom
    return render(request, 'user/register.html', {'form': form,'quotation_roles':quotation_roles})


def forgot_password(request):
    return render(request, 'user/forgot-password.html')

def select_company_fiscal(request):
    company = Company_info.objects.all()
    if request.method == 'POST':
        request.session['company'] = request.POST['sel_company']
        return redirect('home')
    return render(request, 'user/select_company_fiscal.html',{'company':company})


def user_roles(request,pk):
    allow_quotation_roles = quotation_roles()
    user = User.objects.filter(id = pk)
    user_id = User.objects.get(id = pk)
    user_id = Q(user_id = pk)

    form_name = Q(form_name = "Customer")
    allow_role = UserRoles.objects.filter(user_id, form_name).all()

    form_name_supplier = Q(form_name = "Supplier")
    allow_role_supplier = UserRoles.objects.filter(user_id, form_name_supplier).all()

    form_name_transaction = Q(form_name = "Transaction")
    allow_role_transaction = UserRoles.objects.filter(user_id, form_name_transaction).all()

    if request.method == "POST":
        form_id = request.POST.getlist('customer')
        if form_id:
            form_id = 1
        else:
            form_id = 0

        display = request.POST.getlist('display[]')
        add = request.POST.getlist('add[]')
        edit = request.POST.getlist('edit[]')
        delete = request.POST.getlist('delete[]')
        c_print = request.POST.getlist('c_print[]')

        s_display = request.POST.getlist('s_display[]')
        s_add = request.POST.getlist('s_add[]')
        s_edit = request.POST.getlist('s_edit[]')
        s_delete = request.POST.getlist('s_delete[]')
        s_print = request.POST.getlist('s_print[]')

        t_display = request.POST.getlist('t_display[]')
        t_add = request.POST.getlist('t_add[]')
        t_edit = request.POST.getlist('t_edit[]')
        t_delete = request.POST.getlist('t_delete[]')
        t_print = request.POST.getlist('t_print[]')
        t_return = request.POST.getlist('t_return[]')

        for i,value in enumerate(allow_role):
            value.form_id = form_id
            value.save()
            if i == 0:
                matching_display = [c for c in display if "c_rfq_display" in c]
                matching_add = [c for c in add if "c_rfq_add" in c]
                matching_edit = [c for c in edit if "c_rfq_edit" in c]
                matching_delete = [c for c in delete if "c_rfq_delete" in c]
                matching_print = [c for c in c_print if "c_rfq_print" in c]

                if matching_display:
                    value.display = 1
                    value.save()
                else:
                    value.display = 0
                    value.save()
                if matching_add:
                    value.add = 1
                    value.save()
                else:
                    value.add = 0
                    value.save()
                if matching_edit:
                    value.edit = 1
                    value.save()
                else:
                    value.edit = 0
                    value.save()
                if matching_delete:
                    value.delete = 1
                    value.save()
                else:
                    value.delete = 0
                    value.save()
                if matching_print:
                    value.r_print = 1
                    value.save()
                else:
                    value.r_print = 0
                    value.save()
            elif i == 1:
                matching_display = [c for c in display if "c_quotation_display" in c]
                matching_add = [c for c in add if "c_quotation_add" in c]
                matching_edit = [c for c in edit if "c_quotation_edit" in c]
                matching_delete = [c for c in delete if "c_quotation_delete" in c]
                matching_print = [c for c in c_print if "c_quotation_print" in c]

                if matching_display:
                    value.display = 1
                    value.save()
                else:
                    value.display = 0
                    value.save()
                if matching_add:
                    value.add = 1
                    value.save()
                else:
                    value.add = 0
                    value.save()
                if matching_edit:
                    value.edit = 1
                    value.save()
                else:
                    value.edit = 0
                    value.save()
                if matching_delete:
                    value.delete = 1
                    value.save()
                else:
                    value.delete = 0
                    value.save()
                if matching_print:
                    value.r_print = 1
                    value.save()
                else:
                    value.r_print = 0
                    value.save()
            elif i == 2:
                matching_display = [c for c in display if "c_po_display" in c]
                matching_add = [c for c in add if "c_po_add" in c]
                matching_edit = [c for c in edit if "c_po_edit" in c]
                matching_delete = [c for c in delete if "c_po_delete" in c]
                matching_print = [c for c in c_print if "c_po_print" in c]

                if matching_display:
                    value.display = 1
                    value.save()
                else:
                    value.display = 0
                    value.save()
                if matching_add:
                    value.add = 1
                    value.save()
                else:
                    value.add = 0
                    value.save()
                if matching_edit:
                    value.edit = 1
                    value.save()
                else:
                    value.edit = 0
                    value.save()
                if matching_delete:
                    value.delete = 1
                    value.save()
                else:
                    value.delete = 0
                    value.save()
                if matching_print:
                    value.r_print = 1
                    value.save()
                else:
                    value.r_print = 0
                    value.save()
            elif i == 3:
                matching_display = [c for c in display if "c_dc_display" in c]
                matching_add = [c for c in add if "c_dc_add" in c]
                matching_edit = [c for c in edit if "c_dc_edit" in c]
                matching_delete = [c for c in delete if "c_dc_delete" in c]
                matching_print = [c for c in c_print if "c_dc_print" in c]

                if matching_display:
                    value.display = 1
                    value.save()
                else:
                    value.display = 0
                    value.save()
                if matching_add:
                    value.add = 1
                    value.save()
                else:
                    value.add = 0
                    value.save()
                if matching_edit:
                    value.edit = 1
                    value.save()
                else:
                    value.edit = 0
                    value.save()
                if matching_delete:
                    value.delete = 1
                    value.save()
                else:
                    value.delete = 0
                    value.save()
                if matching_print:
                    value.r_print = 1
                    value.save()
                else:
                    value.r_print = 0
                    value.save()

            elif i == 4:
                matching_display = [c for c in display if "c_mrn_display" in c]
                matching_add = [c for c in add if "c_mrn_add" in c]
                matching_edit = [c for c in edit if "c_mrn_edit" in c]
                matching_delete = [c for c in delete if "c_mrn_delete" in c]
                matching_print = [c for c in c_print if "c_mrn_print" in c]

                if matching_display:
                    value.display = 1
                    value.save()
                else:
                    value.display = 0
                    value.save()
                if matching_add:
                    value.add = 1
                    value.save()
                else:
                    value.add = 0
                    value.save()
                if matching_edit:
                    value.edit = 1
                    value.save()
                else:
                    value.edit = 0
                    value.save()
                if matching_delete:
                    value.delete = 1
                    value.save()
                else:
                    value.delete = 0
                    value.save()

                value.r_print = 0
                value.save()

            value.form_id = form_id
            value.save()

        form_id_s = request.POST.getlist('Supplier')
        if form_id_s:
            form_id_s = 2
        else:
            form_id_s = 0

        for i,value in enumerate(allow_role_supplier):
             if i == 0:
                 s_matching_display = [c for c in s_display if "s_rfq_display" in c]
                 s_matching_add = [c for c in s_add if "s_rfq_add" in c]
                 s_matching_edit = [c for c in s_edit if "s_rfq_edit" in c]
                 s_matching_delete = [c for c in s_delete if "s_rfq_delete" in c]
                 s_matching_print = [c for c in s_print if "s_rfq_print" in c]

                 if s_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()
                 if s_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if s_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if s_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if s_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()
             elif i == 1:
                 s_matching_display = [c for c in s_display if "s_quotation_display" in c]
                 s_matching_add = [c for c in s_add if "s_quotation_add" in c]
                 s_matching_edit = [c for c in s_edit if "s_quotation_edit" in c]
                 s_matching_delete = [c for c in s_delete if "s_quotation_delete" in c]
                 s_matching_print = [c for c in s_print if "s_quotation_print" in c]

                 if s_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()

                 if s_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if s_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if s_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if s_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()
             elif i == 2:
                 s_matching_display = [c for c in s_display if "s_po_display" in c]
                 s_matching_add = [c for c in s_add if "s_po_add" in c]
                 s_matching_edit = [c for c in s_edit if "s_po_edit" in c]
                 s_matching_delete = [c for c in s_delete if "s_po_delete" in c]
                 s_matching_print = [c for c in s_print if "s_po_print" in c]

                 if s_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()

                 if s_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if s_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if s_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if s_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()
             elif i == 3:
                 s_matching_display = [c for c in s_display if "s_dc_display" in c]
                 s_matching_add = [c for c in s_add if "s_dc_add" in c]
                 s_matching_edit = [c for c in s_edit if "s_dc_edit" in c]
                 s_matching_delete = [c for c in s_delete if "s_dc_delete" in c]
                 s_matching_print = [c for c in s_print if "s_dc_print" in c]

                 if s_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()
                 if s_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if s_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if s_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if s_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()

             elif i == 4:
                 s_matching_display = [c for c in s_display if "s_mrn_display" in c]
                 s_matching_add = [c for c in s_add if "s_mrn_add" in c]
                 s_matching_edit = [c for c in s_edit if "s_mrn_edit" in c]
                 s_matching_delete = [c for c in s_delete if "s_mrn_delete" in c]
                 s_matching_print = [c for c in s_print if "s_mrn_print" in c]

                 if s_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()
                 if s_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if s_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if s_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()

                     value.r_print = 0
                     value.save()

             value.form_id = form_id_s
             value.save()


        form_id_t = request.POST.getlist('Transaction')
        if form_id_t:
            form_id_t = 3
        else:
            form_id_t = 0

        for i,value in enumerate(allow_role_transaction):
             if i == 0:
                 t_matching_display = [c for c in t_display if "t_coa_display" in c]
                 t_matching_add = [c for c in t_add if "t_coa_add" in c]
                 t_matching_edit = [c for c in t_edit if "t_coa_edit" in c]
                 t_matching_delete = [c for c in t_delete if "t_coa_delete" in c]
                 t_matching_print = [c for c in t_print if "t_coa_print" in c]


                 if t_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()
                 if t_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if t_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if t_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if t_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()

             elif i == 1:
                 t_matching_display = [c for c in t_display if "t_purchase_display" in c]
                 t_matching_add = [c for c in t_add if "t_purchase_add" in c]
                 t_matching_edit = [c for c in t_edit if "t_purchase_edit" in c]
                 t_matching_delete = [c for c in t_delete if "t_purchase_delete" in c]
                 t_matching_print = [c for c in t_print if "t_purchase_print" in c]
                 t_matching_return = [c for c in t_return if "t_purchase_return" in c]


                 if t_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()
                 if t_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if t_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if t_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if t_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()
                 if t_matching_return:
                     value.r_return = 1
                     value.save()
                 else:
                     value.r_return = 0
                     value.save()

             elif i == 2:
                 t_matching_display = [c for c in t_display if "t_pr_display" in c]
                 t_matching_add = [c for c in t_add if "t_pr_add" in c]
                 t_matching_edit = [c for c in t_edit if "t_pr_edit" in c]
                 t_matching_delete = [c for c in t_delete if "t_pr_delete" in c]
                 t_matching_print = [c for c in t_print if "t_pr_print" in c]

                 if t_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()

                 if t_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if t_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if t_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if t_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()
             elif i == 3:
                 t_matching_display = [c for c in t_display if "t_sale_display" in c]
                 t_matching_add = [c for c in t_add if "t_sale_add" in c]
                 t_matching_edit = [c for c in t_edit if "t_sale_edit" in c]
                 t_matching_delete = [c for c in t_delete if "t_sale_delete" in c]
                 t_matching_print = [c for c in t_print if "t_sale_print" in c]
                 t_matching_return = [c for c in t_return if "t_sale_return" in c]


                 if t_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()
                 if t_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if t_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if t_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if t_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()
                 if t_matching_return:
                     value.r_return = 1
                     value.save()
                 else:
                     value.r_return = 0
                     value.save()

             elif i == 4:
                 t_matching_display = [c for c in t_display if "t_sr_display" in c]
                 t_matching_add = [c for c in t_add if "t_sr_add" in c]
                 t_matching_edit = [c for c in t_edit if "t_sr_edit" in c]
                 t_matching_delete = [c for c in t_delete if "t_sr_delete" in c]
                 t_matching_print = [c for c in t_print if "t_sr_print" in c]

                 if t_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()
                 if t_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if t_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if t_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()

                 if t_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()

             if i == 5:
                 t_matching_display = [c for c in t_display if "t_jv_display" in c]
                 t_matching_add = [c for c in t_add if "t_jv_add" in c]
                 t_matching_edit = [c for c in t_edit if "t_jv_edit" in c]
                 t_matching_delete = [c for c in t_delete if "t_jv_delete" in c]
                 t_matching_print = [c for c in t_print if "t_jv_print" in c]

                 if t_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()
                 if t_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if t_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if t_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if t_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()
             elif i == 6:
                 t_matching_display = [c for c in t_display if "t_brv_display" in c]
                 t_matching_add = [c for c in t_add if "t_brv_add" in c]
                 t_matching_edit = [c for c in t_edit if "t_brv_edit" in c]
                 t_matching_delete = [c for c in t_delete if "t_brv_delete" in c]
                 t_matching_print = [c for c in t_print if "t_brv_print" in c]

                 if t_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()

                 if t_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if t_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if t_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if t_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()
             elif i == 7:
                 t_matching_display = [c for c in t_display if "t_crv_display" in c]
                 t_matching_add = [c for c in t_add if "t_crv_add" in c]
                 t_matching_edit = [c for c in t_edit if "t_crv_edit" in c]
                 t_matching_delete = [c for c in t_delete if "t_crv_delete" in c]
                 t_matching_print = [c for c in t_print if "t_crv_print" in c]

                 if t_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()
                 if t_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if t_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if t_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if t_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()
             elif i == 8:
                 t_matching_display = [c for c in t_display if "t_bpv_display" in c]
                 t_matching_add = [c for c in t_add if "t_bpv_add" in c]
                 t_matching_edit = [c for c in t_edit if "t_bpv_edit" in c]
                 t_matching_delete = [c for c in t_delete if "t_bpv_delete" in c]
                 t_matching_print = [c for c in t_print if "t_bpv_print" in c]

                 if t_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()

                 if t_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if t_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if t_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()
                 if t_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()

             elif i == 9:
                 t_matching_display = [c for c in t_display if "t_cpv_display" in c]
                 t_matching_add = [c for c in t_add if "t_cpv_add" in c]
                 t_matching_edit = [c for c in t_edit if "t_cpv_edit" in c]
                 t_matching_delete = [c for c in t_delete if "t_cpv_delete" in c]
                 t_matching_print = [c for c in t_print if "t_cpv_print" in c]

                 if t_matching_display:
                     value.display = 1
                     value.save()
                 else:
                     value.display = 0
                     value.save()
                 if t_matching_add:
                     value.add = 1
                     value.save()
                 else:
                     value.add = 0
                     value.save()
                 if t_matching_edit:
                     value.edit = 1
                     value.save()
                 else:
                     value.edit = 0
                     value.save()
                 if t_matching_delete:
                     value.delete = 1
                     value.save()
                 else:
                     value.delete = 0
                     value.save()

                 if t_matching_print:
                     value.r_print = 1
                     value.save()
                 else:
                     value.r_print = 0
                     value.save()

             value.form_id = form_id_t
             value.save()


    return render(request, 'user/user_roles.html',{'user':user,'allow_role':allow_role,'allow_role_supplier':allow_role_supplier,'allow_quotation_roles':allow_quotation_roles,'allow_role_transaction':allow_role_transaction})

def user_list(request):
    allow_quotation_roles = quotation_roles()
    all_user = User.objects.all()
    return render(request, 'user/users.html',{'all_user':all_user,'allow_quotation_roles':allow_quotation_roles})
