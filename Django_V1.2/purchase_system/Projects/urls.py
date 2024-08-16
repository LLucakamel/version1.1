from django.urls import path
from .views import project_list, add_project, product_details, edit_project, import_projects, export_projects, search_projects

urlpatterns = [
    path('', project_list, name='project-list'),
    path('add/', add_project, name='add-project'),
    path('details/<int:project_id>/', product_details, name='product-details'),
    path('edit-project/<int:project_id>/', edit_project, name='edit-project'),
    path('projects/import/', import_projects, name='import-projects'),
    path('projects/export/', export_projects, name='export-projects'),
    path('search/', search_projects, name='search-projects'),
]