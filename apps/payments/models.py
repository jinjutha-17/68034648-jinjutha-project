from django.db import models
from apps.tenants.models import Tenant
from apps.rooms.models import Room


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    PAYMENT_TYPES = [
        ('rent', 'Rent'),
        ('deposit', 'Deposit'),
        ('utility', 'Utility'),
        ('other', 'Other'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='rent')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.tenant} - {self.get_payment_type_display()} - {self.due_date}"


class Meter(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='meters')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='meters')
    previous_reading = models.DecimalField(max_digits=10, decimal_places=2)
    current_reading = models.DecimalField(max_digits=10, decimal_places=2)
    units_consumed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    reading_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reading_date']

    def save(self, *args, **kwargs):
        self.units_consumed = self.current_reading - self.previous_reading
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Meter Reading - {self.tenant} - {self.reading_date}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='invoices')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='invoices')
    invoice_date = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-invoice_date']

    def __str__(self):
        return f"Invoice - {self.tenant} - {self.invoice_date}"


class Maintenance(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='maintenances')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenances')
    issue = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reported_date = models.DateField(auto_now_add=True)
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reported_date']

    def __str__(self):
        return f"Maintenance - {self.tenant} - {self.issue}"
