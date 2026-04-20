from django.db import models
from django.contrib.auth.models import User
from apps.rooms.models import Room
from apps.tenants.models import Tenant

class Parcel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'ค้างรับ'),
        ('received', 'รับจ่ายแล้ว'),
    ]
    
    COURIER_CHOICES = [
        ('Kerry', 'Kerry Express'),
        ('ThaiPost', 'ไปรษณีย์ไทย (ThaiPost)'),
        ('Shopee', 'Shopee Express'),
        ('Flash', 'Flash Express'),
        ('Lazada', 'Lazada Logistics'),
        ('J&T', 'J&T Express'),
        ('Ninja', 'Ninja Van'),
        ('Other', 'อื่นๆ'),
    ]
    
    TYPE_CHOICES = [
        ('กล่องใหญ่', 'กล่องใหญ่'),
        ('กล่องเล็ก', 'กล่องเล็ก'),
        ('ห่อใหญ่', 'ห่อใหญ่'),
        ('ห่อเล็ก', 'ห่อเล็ก'),
        ('ซองใหญ่', 'ซองใหญ่'),
        ('ซองเล็ก', 'ซองเล็ก'),
        ('อื่นๆ', 'อื่นๆ'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='parcels')
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True, related_name='parcels')
    tracking_number = models.CharField(max_length=100)
    courier = models.CharField(max_length=50, choices=COURIER_CHOICES, default='Kerry')
    parcel_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='กล่องเล็ก')
    parcel_image = models.ImageField(upload_to='parcels/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    received_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_parcels')

    class Meta:
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.tracking_number} - {self.room.room_number}"
