import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.tenants.models import UserProfile

def restore_accounts():
    accounts = [
        {'email': 'admin@test.com', 'username': 'admin', 'password': '1234', 'role': 'Admin', 'is_superuser': True, 'is_staff': True},
        {'email': 'staff@test.com', 'username': 'staff', 'password': '4321', 'role': 'Staff', 'is_superuser': False, 'is_staff': True},
        {'email': 'client@test.com', 'username': 'client', 'password': '1122', 'role': 'Tenant', 'is_superuser': False, 'is_staff': False},
    ]
    
    print("--- Restoring Original Accounts ---")
    for acc in accounts:
        user = User.objects.filter(email=acc['email']).first()
        if not user:
            user = User.objects.filter(username=acc['username']).first()
            
        if not user:
            user = User.objects.create_user(
                username=acc['username'],
                email=acc['email'],
                password=acc['password']
            )
            status = "Created"
        else:
            user.set_password(acc['password'])
            user.username = acc['username']
            user.email = acc['email']
            status = "Updated"
            
        user.is_superuser = acc['is_superuser']
        user.is_staff = acc['is_staff']
        user.save()
        
        # Ensure profile exists with correct role
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = acc['role']
        profile.save()
        
        print(f" - [{status}] {acc['email']} with role {acc['role']}")

if __name__ == "__main__":
    restore_accounts()
