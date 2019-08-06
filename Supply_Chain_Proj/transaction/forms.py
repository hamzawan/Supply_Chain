from supplier.models import Company_info
from django import forms

class CompanyUpdateForm(forms.ModelForm):
  email = forms.EmailField(required=False)
  company_address = forms.CharField(widget=forms.Textarea,required=False)
  company_logo = forms.CharField(widget=forms.Textarea,required=False)
  phone_no = forms.CharField(required=False)
  mobile_no = forms.CharField(required=False)
  website = forms.CharField(required=False)
  ntn = forms.CharField(required=False)
  stn = forms.CharField(required=False)
  cnic = forms.CharField(required=False)  

  class Meta:
    model = Company_info
    fields = [    'company_name', 
    'company_address',
    'company_logo',
    'phone_no', 
    'mobile_no', 
    'email', 
    'website', 
    'ntn', 
    'stn', 
    'cnic']


 