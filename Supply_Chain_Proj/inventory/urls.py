from django.urls import path, include
from . import views

urlpatterns = [
    path('item_stock/', views.item_stock, name = 'item-stock'),
    path('add_product/', views.add_product, name = 'add-product'),
    path('edit_item/<pk>/', views.edit_item, name = 'edit-item'),
    path('delete_item/<pk>/', views.delete_item, name = 'delete-item'),

    path('categories/', views.categories, name = 'categories'),

    path('categories/main/new', views.main_categories, name = 'main-categories'),
    path('categories/main/edit', views.edit_main_categories, name = 'edit-main-categories'),
    path('categories/main/delete/<pk>', views.delete_categories, name = 'delete-categories'),

    path('categories/sub/new', views.sub_categories, name = 'sub-categories'),
    path('categories/sub/edit', views.edit_sub_categories, name = 'edit-sub-categories'),
    path('categories/sub/delete/<pk>', views.delete_sub_categories, name = 'delete-sub-categories'),

]
