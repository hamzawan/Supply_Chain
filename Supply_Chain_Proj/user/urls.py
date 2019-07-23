from django.urls import path, include
from . import views


urlpatterns = [

    path('select_company_fiscal', views.select_company_fiscal, name = 'company-fiscal'),
    path('user_roles/<pk>', views.user_roles, name = 'user-roles'),
    path('user_list/', views.user_list, name = 'user-list'),
]
