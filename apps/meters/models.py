from decimal import Decimal
from django.db import models
from apps.rooms.models import Room
from apps.tenants.models import Tenant

class Meter(models.Model):
    ELECTRIC_RATE = Decimal('7.00')
    WATER_RATE = Decimal('18.00')

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True)

    reading_value = models.DecimalField(max_digits=10, decimal_places=2)  # หน่วยไฟ
    water_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

    reading_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        rent = self.room.monthly_rent if self.room else Decimal('0.00')
        electric = (self.reading_value or 0) * self.ELECTRIC_RATE
        water = (self.water_charge or 0) * self.WATER_RATE
        return (rent + electric + water).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        # 🔥 auto set tenant จาก room
        if self.room and hasattr(self.room, 'current_tenant'):
            self.tenant = self.room.current_tenant

        self.total_amount = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Room {self.room.room_number} - {self.reading_date}"