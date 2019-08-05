from django.urls import path, include
from . import views


urlpatterns = [

    path('select_company_fiscal', views.select_company_fiscal, name = 'company-fiscal'),
    path('user_roles/<pk>', views.user_roles, name = 'user-roles'),
    path('user_list/', views.user_list, name = 'user-list'),
    path('user_roles/delete/<pk>', views.delete_user_roles, name = 'delete-user-roles'),
    path('user/edit/<pk>', views.edit_user, name = 'edit-user-roles'),
]
