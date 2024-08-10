from django.shortcuts import render, redirect, get_object_or_404  # Added get_object_or_404 here
from .models import Project
from .forms import ProjectForm  # Import ProjectForm from forms.py within the same directory

def project_create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        code = request.POST.get('code')
        location = request.POST.get('location')
        consultant = request.POST.get('consultant')
        stage = request.POST.get('stage')
        Project.objects.create(name=name, code=code, location=location, consultant=consultant, stage=stage)
        return redirect('some-view-name')
    return render(request, 'projects.html')

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project-list')  # Redirect to the project list after saving
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})

from django.http import JsonResponse

def product_details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return JsonResponse({
        'name': project.name,
        'code': project.code,
        'location': project.location,
        'consultant': project.consultant
    })

def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('some-view-name')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form})