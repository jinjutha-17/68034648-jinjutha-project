from django.db import models


class Room(models.Model):
    ROOM_TYPES = [
        ('รายเดือน', 'รายเดือน'),
        ('รายวัน', 'รายวัน'),
    ]
    STATUS_CHOICES = [
        ('ว่าง', 'ว่าง'),
        ('ไม่ว่าง', 'ไม่ว่าง'),
        ('ซ่อมบำรุง', 'ซ่อมบำรุง'),
    ]

    room_number = models.CharField(max_length=20, unique=True)
    floor = models.PositiveIntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='รายเดือน')
    size_sqm = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    elec_rate = models.DecimalField(max_digits=5, decimal_places=2, default=7.00)
    water_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ว่าง')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['floor', 'room_number']

    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"
