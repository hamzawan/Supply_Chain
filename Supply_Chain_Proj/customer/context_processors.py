from django.http import request
from user.models import Company_info


def company_name_processor(request):
    names = Company_info.objects.all()
    return {'names':names}
