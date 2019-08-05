from django.http import request
from user.models import Company_info


def company_name_processor(request):
    company = request.session['company']
    names = Company_info.objects.filter(id=company).first()
    return {'names':names}
