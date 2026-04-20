from django.db import models
from apps.rooms.models import Room


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.pk} - {self.full_name} ({self.room})"

    @property
    def duration_days(self):
        return (self.check_out_date - self.check_in_date).days
