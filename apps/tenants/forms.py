from django import forms
from .models import Tenant
from apps.rooms.models import Room


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'id_card',
            'emergency_contact', 'emergency_phone', 'room',
            'move_in_date', 'move_out_date', 'is_active', 'notes'
        ]
        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
            'move_out_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # แสดงเฉพาะห้องว่าง + ห้องที่ผู้เช่าคนนี้อยู่อยู่แล้ว (กรณี edit)
        if self.instance and self.instance.pk and self.instance.room:
            self.fields['room'].queryset = Room.objects.filter(
                status='ว่าง'
            ) | Room.objects.filter(pk=self.instance.room.pk)
        else:
            self.fields['room'].queryset = Room.objects.filter(status='ว่าง')

        # แสดงชื่อห้องให้ชัดเจน
        self.fields['room'].label_from_instance = lambda r: (
            f"ห้อง {r.room_number} (ชั้น {r.floor}) — {r.monthly_rent} บาท/เดือน"
        )
        self.fields['room'].empty_label = "— เลือกห้อง —"
