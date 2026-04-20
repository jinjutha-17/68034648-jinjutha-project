from django.db import models
from apps.rooms.models import Room
from apps.meters.models import Meter

class MeterReading(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    prev_elec = models.FloatField(default=0)
    curr_elec = models.FloatField(default=0)
    prev_water = models.FloatField(default=0)
    curr_water = models.FloatField(default=0)
    reading_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"มิเตอร์ {self.room.room_number} - {self.reading_date}"


class Billing(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, null=True, blank=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    service_month = models.DateField(auto_now_add=True)

    is_paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"บิล {self.room.room_number}"