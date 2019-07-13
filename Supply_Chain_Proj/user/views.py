from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegistrationFrom
from  supplier.models import Company_info


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = RegistrationFrom
    return render(request, 'user/register.html', {'form': form})


def forgot_password(request):
    return render(request, 'user/forgot-password.html')

def select_company_fiscal(request):
    company = Company_info.objects.all()
    if request.method == 'POST':
        request.session['company'] = request.POST['sel_company']
        return redirect('home')
    return render(request, 'user/select_company_fiscal.html',{'company':company})
