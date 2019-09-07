from django.http import request
from user.models import Company_info


def company_name_processor(request):
    if request.session._session:
        company = request.session['company']
        names = Company_info.objects.filter(id=company).first()
        return {'names':names}
    else:
        request.session['company'] = 1
        company = request.session['company']
        names = Company_info.objects.filter(id=company).first()
        return {'names':names}


def change_company(request):
    all_company = Company_info.objects.all()
    return {'all_company':all_company}
