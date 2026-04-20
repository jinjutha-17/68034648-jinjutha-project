import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.tenants.models import UserProfile, EmployeePermission

def force_restore():
    accounts = [
        {
            'email': 'admin@test.com', 
            'username': 'admin', 
            'password': '1234', 
            'role': 'Admin', 
            'is_superuser': True, 
            'is_staff': True
        },
        {
            'email': 'staff@test.com', 
            'username': 'staff', 
            'password': '4321', 
            'role': 'Staff', 
            'is_superuser': False, 
            'is_staff': True
        },
        {
            'email': 'client@test.com', 
            'username': 'client', 
            'password': '1122', 
            'role': 'Tenant', 
            'is_superuser': False, 
            'is_staff': False
        },
    ]
    
    print("--- FORCE RESTORING ORIGINAL ACCOUNTS ---")
    for acc in accounts:
        # 1. Clean up existing users to avoid IntegrityErrors
        User.objects.filter(email=acc['email']).delete()
        User.objects.filter(username=acc['username']).delete()
        
        # 2. Create the user
        if acc['is_superuser']:
            user = User.objects.create_superuser(
                username=acc['username'],
                email=acc['email'],
                password=acc['password']
            )
        else:
            user = User.objects.create_user(
                username=acc['username'],
                email=acc['email'],
                password=acc['password']
            )
        
        user.is_staff = acc['is_staff']
        user.save()
        
        # 3. Handle UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = acc['role']
        profile.save()
        
        # 4. Handle Employee Permissions (for Admin and Staff)
        if acc['role'] in ['Admin', 'Staff']:
            perm, _ = EmployeePermission.objects.get_or_create(user=user)
            perm.can_manage_rooms = True
            perm.can_manage_tenants = True
            perm.can_manage_billing = True
            perm.can_manage_payments = True
            perm.can_confirm_payment = True
            perm.can_manage_parcels = True
            perm.can_manage_maintenance = True
            perm.can_view_reports = True
            perm.can_manage_settings = True
            perm.save()
            
        print(f" - [FORCED] {acc['email']} (User: {acc['username']}) restored as {acc['role']}")

    print("\nAccount restoration complete. You can now login with these credentials.")

if __name__ == "__main__":
    force_restore()
