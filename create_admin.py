import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.tenants.models import UserProfile, EmployeePermission

email = 'admin@test.com'
password = '1234'
username = 'admin'

user, created = User.objects.get_or_create(username=username)
user.email = email
user.set_password(password)
user.is_superuser = True
user.is_staff = True
user.save()

# Create or Update UserProfile
profile, created = UserProfile.objects.get_or_create(user=user)
profile.role = 'Admin'
profile.save()

# Create or Update EmployeePermission
permission, created = EmployeePermission.objects.get_or_create(user=user)
permission.can_manage_rooms = True
permission.can_manage_tenants = True
permission.can_manage_billing = True
permission.can_manage_payments = True
permission.can_confirm_payment = True
permission.can_manage_parcels = True
permission.can_manage_maintenance = True
permission.can_view_reports = True
permission.can_manage_settings = True
permission.save()

print(f"Superuser {username} and associated profiles created/updated successfully.")
