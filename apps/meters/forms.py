from django import forms
from .models import Meter

class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['room', 'reading_value', 'water_charge', 'reading_date']