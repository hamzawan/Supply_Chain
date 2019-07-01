from django.urls import path, include
from . import views

urlpatterns = [
    path('item_stock/', views.item_stock, name = 'item-stock'),
    path('new/', views.new_item_stock, name = 'new-item-stock'),
    path('add_product/', views.add_product, name = 'add-product'),
    path('edit_item/<pk>/', views.edit_item, name = 'edit-item'),

]
