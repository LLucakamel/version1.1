from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('new/', views.product_create, name='product_new'),
    path('edit/<int:id>/', views.product_update, name='product_edit'),
    path('delete/<int:id>/', views.product_delete, name='product_delete'),
    path('export/', views.product_export, name='product_export'),
    path('import/', views.product_import, name='product_import'),
]