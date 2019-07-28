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
    if request.method == "POST":
        form_id = request.POST.getlist('customer')
        if form_id:
            form_id = 1
        else:
            form_id = 0
        add = request.POST.getlist('add[]')
        edit = request.POST.getlist('edit[]')
        delete = request.POST.getlist('delete[]')
        c_print = request.POST.getlist('c_print[]')
        print(add)
        s_add = request.POST.getlist('s_add[]')
        s_edit = request.POST.getlist('s_edit[]')
        s_delete = request.POST.getlist('s_delete[]')
        s_print = request.POST.getlist('s_print[]')

        for i,value in enumerate(allow_role):
            value.form_id = form_id
            value.save()
            if i == 0:
                matching_add = [c for c in add if "c_rfq_add" in c]
                matching_edit = [c for c in edit if "c_rfq_edit" in c]
                matching_delete = [c for c in delete if "c_rfq_delete" in c]
                matching_print = [c for c in c_print if "c_rfq_print" in c]
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
                matching_add = [c for c in add if "c_quotation_add" in c]
                matching_edit = [c for c in edit if "c_quotation_edit" in c]
                matching_delete = [c for c in delete if "c_quotation_delete" in c]
                matching_print = [c for c in c_print if "c_quotation_print" in c]
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
                matching_add = [c for c in add if "c_po_add" in c]
                matching_edit = [c for c in edit if "c_po_edit" in c]
                matching_delete = [c for c in delete if "c_po_delete" in c]
                matching_print = [c for c in c_print if "c_po_print" in c]
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
                    value.edit = 0
                    value.save()
                if matching_print:
                    value.r_print = 1
                    value.save()
                else:
                    value.r_print = 0
                    value.save()
            elif i == 3:
                matching_add = [c for c in add if "c_dc_add" in c]
                matching_edit = [c for c in edit if "c_dc_edit" in c]
                matching_delete = [c for c in delete if "c_dc_delete" in c]
                matching_print = [c for c in c_print if "c_dc_print" in c]
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
        #
        #
        # for i,value in enumerate(allow_role_supplier):
        #     if i == 0:
        #         s_matching_add = [c for c in s_add if "s_rfq_add" in c]
        #         s_matching_edit = [c for c in s_edit if "s_rfq_edit" in c]
        #         s_matching_delete = [c for c in s_delete if "s_rfq_delete" in c]
        #         s_matching_print = [c for c in s_print if "s_rfq_print" in c]
        #
        #         if s_matching_add:
        #             value.add = 1
        #             value.save()
        #         else:
        #             value.add = 0
        #             value.save()
        #         if s_matching_edit:
        #             value.edit = 1
        #             value.save()
        #         else:
        #             value.edit = 0
        #             value.save()
        #         if s_matching_delete:
        #             value.delete = 1
        #             value.save()
        #         else:
        #             value.delete = 0
        #             value.save()
        #         if s_matching_print:
        #             value.r_print = 1
        #             value.save()
        #         else:
        #             value.delete = 0
        #             value.save()
            # elif i == 1:
            #     matching_add = [c for c in add if "c_quotation_add" in c]
            #     matching_edit = [c for c in edit if "c_quotation_edit" in c]
            #     matching_delete = [c for c in delete if "c_quotation_delete" in c]
            #     matching_print = [c for c in print if "c_quotation_print" in c]
            #     if matching_add:
            #         value.add = 1
            #         value.save()
            #     else:
            #         value.add = 0
            #         value.save()
            #     if matching_edit:
            #         value.edit = 1
            #         value.save()
            #     else:
            #         value.edit = 0
            #         value.save()
            #     if matching_delete:
            #         value.delete = 1
            #         value.save()
            #     else:
            #         value.delete = 0
            #         value.save()
            #     if matching_print:
            #         value.r_print = 1
            #         value.save()
            #     else:
            #         value.r_print = 0
            #         value.save()
            # elif i == 2:
            #     matching_add = [c for c in add if "c_po_add" in c]
            #     matching_edit = [c for c in edit if "c_po_edit" in c]
            #     matching_delete = [c for c in delete if "c_po_delete" in c]
            #     matching_print = [c for c in print if "c_po_print" in c]
            #     if matching_add:
            #         value.add = 1
            #         value.save()
            #     else:
            #         value.add = 0
            #         value.save()
            #     if matching_edit:
            #         value.edit = 1
            #         value.save()
            #     else:
            #         value.edit = 0
            #         value.save()
            #     if matching_delete:
            #         value.delete = 1
            #         value.save()
            #     else:
            #         value.edit = 0
            #         value.save()
            #     if matching_print:
            #         value.r_print = 1
            #         value.save()
            #     else:
            #         value.r_print = 0
            #         value.save()
            # elif i == 3:
            #     matching_add = [c for c in add if "c_dc_add" in c]
            #     matching_edit = [c for c in edit if "c_dc_edit" in c]
            #     matching_delete = [c for c in delete if "c_dc_delete" in c]
            #     matching_print = [c for c in print if "c_dc_print" in c]
            #     if matching_add:
            #         value.add = 1
            #         value.save()
            #     else:
            #         value.add = 0
            #         value.save()
            #     if matching_edit:
            #         value.edit = 1
            #         value.save()
            #     else:
            #         value.edit = 0
            #         value.save()
            #     if matching_delete:
            #         value.delete = 1
            #         value.save()
            #     else:
            #         value.delete = 0
            #         value.save()
            #     if matching_print:
            #         value.r_print = 1
            #         value.save()
            #     else:
            #         value.r_print = 0
            #         value.save()

    return render(request, 'user/user_roles.html',{'user':user,'allow_role':allow_role,'allow_role_supplier':allow_role_supplier,'allow_quotation_roles':allow_quotation_roles})

def user_list(request):
    allow_quotation_roles = quotation_roles()
    all_user = User.objects.all()
    return render(request, 'user/users.html',{'all_user':all_user,'allow_quotation_roles':allow_quotation_roles})
