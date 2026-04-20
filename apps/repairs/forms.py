from django import forms
from .models import Repair


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['room', 'issue', 'description', 'priority', 'status', 'completed_date', 'notes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
            'completed_date': forms.DateInput(attrs={'type': 'date'}),
        }
