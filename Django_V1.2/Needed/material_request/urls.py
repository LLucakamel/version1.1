from django.urls import path
from .views import material_request_view, add_material_request

urlpatterns = [
    path('material-request/', material_request_view, name='material_request'),
    path('add/', add_material_request, name='add_material_request'),
]