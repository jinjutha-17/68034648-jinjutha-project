import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

def verify():
    print("--- Database Verification ---")
    
    # 1. Check Connection
    try:
        connection.ensure_connection()
        print("SUCCESS: Connected to PostgreSQL database.")
    except Exception as e:
        print(f"FAILED: Connection error: {e}")
        return

    # 2. Check Users
    test_emails = ['admin@test.com', 'staff@test.com', 'client@test.com']
    print("\nChecking Original Accounts:")
    found_all = True
    for email in test_emails:
        user = User.objects.filter(email=email).first()
        if user:
            print(f" - [FOUND]  {email} (ID: {user.id})")
        else:
            print(f" - [MISSING] {email}")
            found_all = False
            
    if found_all:
        print("\nALL ORIGINAL ACCOUNTS ARE PRESENT.")
    else:
        print("\nWARNING: Some original accounts are missing. You may need to seed the data.")

    # 3. Check for specific Views/Triggers
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM information_schema.views WHERE table_name = 'v_dashboard_summary';")
        view_exists = cursor.fetchone()[0] > 0
        print(f"DASHBOARD VIEW EXISTS: {'YES' if view_exists else 'NO'}")

if __name__ == "__main__":
    verify()
