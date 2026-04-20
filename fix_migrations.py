import os
import django
from django.db import connection

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment_project.settings')
django.setup()

def fix_migrations_table():
    with connection.cursor() as cursor:
        print("Checking django_migrations table...")
        
        # Check current structure
        cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'django_migrations'")
        for row in cursor.fetchall():
            print(f"Column: {row[0]}, Type: {row[1]}")
        
        # Backup data
        cursor.execute("SELECT app, name, applied INTO #temp_migrations FROM django_migrations")
        print("Backed up migration data")
        
        # Drop and recreate table
        cursor.execute("DROP TABLE django_migrations")
        cursor.execute("""
            CREATE TABLE django_migrations (
                id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
                app nvarchar(255) NOT NULL,
                name nvarchar(255) NOT NULL,
                applied datetime2 NOT NULL
            )
        """)
        print("Recreated table with datetime2")
        
        # Restore data
        cursor.execute("INSERT INTO django_migrations (app, name, applied) SELECT app, name, applied FROM #temp_migrations")
        cursor.execute("DROP TABLE #temp_migrations")
        print("Restored migration data")

if __name__ == "__main__":
    fix_migrations_table()