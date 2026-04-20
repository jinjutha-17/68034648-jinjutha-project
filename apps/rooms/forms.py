from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'floor', 'room_type', 'size_sqm', 'monthly_rent', 'status', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
