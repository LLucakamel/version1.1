from django.shortcuts import render, redirect
from django.http import JsonResponse
from Projects.models import Project  # Import the Project model
from django.shortcuts import render
from .forms import MaterialRequestForm
from .models import MaterialRequest
from django.utils import timezone

def material_request_view(request):
    # Your logic here, for example, fetching data to be displayed
    return render(request, 'material_request/material_request.html')


def add_material_request(request):
    # Logic to generate a unique material request number
    material_request_number = MaterialRequest.objects.count() + 1
    
    if request.method == 'POST':
        form = MaterialRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material_request')
    else:
        form = MaterialRequestForm()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        project_id = request.GET.get('project_id')
        project = Project.objects.get(id=project_id)
        data = {
            'code': project.code,
            'location': project.location,
            'consultant': project.consultant,
            # 'stage': project.stage
        }
        return JsonResponse(data)

    context = {
        'form': form,
        'material_request_number': material_request_number,
        'today': timezone.now().date()
    }

    return render(request, 'material_request/add_material_request.html', context)


