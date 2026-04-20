from django.db import models

from apps.rooms.models import Room
from apps.tenants.models import Tenant


class Repair(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repairs',
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='repairs'
    )

    # ของเดิม
    issue = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reported_date = models.DateField(auto_now_add=True)
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # เพิ่มจาก RepairRequest
    category = models.CharField(max_length=50, blank=True)
    category_label = models.CharField(max_length=100, blank=True)
    is_seen_by_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['-reported_date', '-created_at']

    def __str__(self):
        room_number = self.room.room_number if self.room else 'No Room'
        return f"Repair - {room_number} - {self.issue}"