from django.urls import path, include
from . import views


urlpatterns = [

    path('select_company_fiscal', views.select_company_fiscal, name = 'company-fiscal'),
]
