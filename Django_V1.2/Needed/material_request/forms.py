from django import forms
from .models import MaterialRequest
from Projects.models import Project

class MaterialRequestForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), required=True)

    class Meta:
        model = MaterialRequest
        fields = ['request_date', 'supply_date', 'project', 'project_code', 'project_location', 'project_consultant', 'project_stage']