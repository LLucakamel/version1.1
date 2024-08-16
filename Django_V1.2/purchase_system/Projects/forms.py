from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'code', 'consultant', 'location']
        labels = {
            'name': 'Project Name',
            'code': 'Project Code',
            'consultant': 'Project Consultant',
            'location': 'Project Location'
        }