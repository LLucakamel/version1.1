from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    path('new/', views.order_create, name='order_create'),
    path('order/update/<int:id>/', views.order_update, name='order_update'),
    path('delete/<int:id>/', views.delete_order, name='order_delete'),
    path('approve/<int:id>/', views.order_approve, name='order_approve'),
    path('disapprove/<int:id>/', views.order_disapprove, name='order_disapprove'),
    path('product-search/', views.product_search, name='product_search'),
    path('order/review/<int:order_id>/', views.order_review, name='order_review'),
    path('project-search/', views.project_search, name='project_search'),
]