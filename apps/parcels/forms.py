from django import forms
from .models import Parcel
from apps.rooms.models import Room

class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['room', 'tracking_number', 'courier', 'parcel_type', 'parcel_image']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select select2'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'กรอกหมายเลข Tracking'}),
            'courier': forms.Select(attrs={'class': 'form-select'}),
            'parcel_type': forms.Select(attrs={'class': 'form-select'}),
            'parcel_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ParcelForm, self).__init__(*args, **kwargs)
        # Only show occupied rooms for parcel delivery
        self.fields['room'].queryset = Room.objects.filter(status='ไม่ว่าง').order_by('room_number')
