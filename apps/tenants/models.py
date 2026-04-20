from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.rooms.models import Room


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Tenant', 'Tenant'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Tenant')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class EmployeePermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_permission')
    can_manage_rooms = models.BooleanField(default=False)
    can_manage_tenants = models.BooleanField(default=False)
    can_manage_billing = models.BooleanField(default=False)
    can_manage_payments = models.BooleanField(default=False)
    can_confirm_payment = models.BooleanField(default=False)
    can_manage_parcels = models.BooleanField(default=False)
    can_manage_maintenance = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    can_manage_settings = models.BooleanField(default=False)

    def __str__(self):
        return f"Permissions for {self.user.username}"


class Tenant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    id_card = models.CharField(max_length=50, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    room = models.OneToOneField(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_tenant'
    )
    move_in_date = models.DateField(null=True, blank=True)
    move_out_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Contract(models.Model):
    STATUS_CHOICES = [
        ('active', 'ใช้งานอยู่'),
        ('expired', 'หมดสัญญา'),
        ('terminated', 'ยกเลิก'),
    ]

    contract_id = models.CharField(max_length=20, blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='contracts')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='contracts')
    contract_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    document = models.FileField(upload_to='contracts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.contract_id:
            next_number = Contract.objects.count() + 1
            self.contract_id = f"LD-{next_number}"

        today = timezone.now().date()
        if self.status != 'terminated':
            if self.end_date < today:
                self.status = 'expired'
                self.is_active = False
            else:
                self.status = 'active'
                self.is_active = True

        super().save(*args, **kwargs)

    @property
    def days_remaining(self):
        return (self.end_date - timezone.now().date()).days

    def __str__(self):
        return f"{self.contract_id} - {self.tenant.full_name} - Room {self.room.room_number}"