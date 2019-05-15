from django.urls import path, include
from . import views


urlpatterns = [
    path('purchase/', views.purchase, name = 'purchase'),
    path('purchase/new/', views.new_purchase, name = 'new-purchase'),

]
