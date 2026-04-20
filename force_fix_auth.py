import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.tenants.models import UserProfile, EmployeePermission

def force_fix():
    email = 'admin@test.com'
    password = '1234'
    # We use the email as the username to bridge the gap between UI test accounts and Django's default auth
    username = 'admin@test.com'

    print(f"--- Force Fixing User: {username} ---")

    # 1. Create/Update User
    user, created = User.objects.get_or_create(username=username)
    user.email = email
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.save()
    
    status = "Created" if created else "Updated"
    print(f"[+] User '{username}' {status} and Password set to '{password}'")

    # 2. Ensure UserProfile (Admin Role)
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.role = 'Admin'
    profile.save()
    print(f"[+] UserProfile set to 'Admin'")

    # 3. Ensure EmployeePermission (Full Access)
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
    print(f"[+] EmployeePermissions granted (All set to True)")

    # 4. Cleanup old 'admin' if it exists (optional but cleaner)
    # User.objects.filter(username='admin').delete()
    # print("[i] Cleanup: Old 'admin' username removed to avoid confusion.")

    print("\n[SUCCESS] Login should now work using:")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("---------------------------------------")

if __name__ == "__main__":
    force_fix()
