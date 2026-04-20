import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment_project.settings')
django.setup()

def clean_db():
    print("--- Cleaning Database Objects (Views & Triggers) ---")
    with connection.cursor() as cursor:
        # 1. Drop all Views
        cursor.execute("""
            SELECT viewname FROM pg_views WHERE schemaname = 'public';
        """)
        views = cursor.fetchall()
        for view in views:
            view_name = view[0]
            print(f"Dropping View: {view_name}")
            cursor.execute(f"DROP VIEW IF EXISTS {view_name} CASCADE;")

        # 2. Drop all Triggers (Custom ones)
        # We look for triggers that are not internal
        cursor.execute("""
            SELECT tgname, relname 
            FROM pg_trigger t
            JOIN pg_class c ON t.tgrelid = c.oid
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = 'public' AND t.tgisinternal = false;
        """)
        triggers = cursor.fetchall()
        for tg, table in triggers:
            print(f"Dropping Trigger: {tg} on table {table}")
            cursor.execute(f"DROP TRIGGER IF EXISTS {tg} ON {table} CASCADE;")

    print("Cleanup Complete.")

if __name__ == "__main__":
    clean_db()
