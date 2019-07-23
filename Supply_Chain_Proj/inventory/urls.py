from django.urls import path, include
from . import views

urlpatterns = [
    path('item_stock/', views.item_stock, name = 'item-stock'),
    path('add_product/', views.add_product, name = 'add-product'),
    path('edit_item/<pk>/', views.edit_item, name = 'edit-item'),
    path('delete_item/<pk>/', views.delete_item, name = 'delete-item'),

]
