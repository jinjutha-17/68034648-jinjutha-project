import os
import django
from django.db import connection

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment_project.settings')
django.setup()

def run_sql():
    with connection.cursor() as cursor:
        print("Starting SQL Object Creation...")
        
        # 1. Create View v_TenantDashboard
        print("Creating View v_TenantDashboard...")
        cursor.execute("IF EXISTS (SELECT * FROM sys.views WHERE name = 'v_TenantDashboard') DROP VIEW v_TenantDashboard;")
        cursor.execute("""
            CREATE VIEW v_TenantDashboard AS
            SELECT 
                t.id AS TenantID,
                t.email AS TenantEmail,
                t.first_name + ' ' + t.last_name AS FullName,
                r.room_number AS RoomNumber,
                ISNULL((SELECT SUM(b.amount) FROM payments_invoice b WHERE b.tenant_id = t.id AND b.status != 'paid'), 0) AS BalanceDue
            FROM tenants_tenant t
            LEFT JOIN rooms_room r ON t.room_id = r.id;
        """)
        
        # 2. Create Trigger trg_UpdateRoomStatus
        print("Creating Trigger trg_UpdateRoomStatus...")
        cursor.execute("IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_UpdateRoomStatus') DROP TRIGGER trg_UpdateRoomStatus;")
        cursor.execute("""
            CREATE TRIGGER trg_UpdateRoomStatus 
            ON tenants_contract
            AFTER INSERT
            AS
            BEGIN
                UPDATE r
                SET r.status = N'ไม่ว่าง'
                FROM rooms_room r
                JOIN inserted i ON r.id = i.room_id;
            END;
        """)
        
        print("Verification: Checking if objects exist...")
        cursor.execute("SELECT name FROM sys.views WHERE name = 'v_TenantDashboard';")
        view_exists = cursor.fetchone()
        cursor.execute("SELECT name FROM sys.triggers WHERE name = 'trg_UpdateRoomStatus';")
        trigger_exists = cursor.fetchone()
        
        if view_exists: print(f"SUCCESS: View '{view_exists[0]}' created.")
        else: print("FAILED: View not found.")
        
        if trigger_exists: print(f"SUCCESS: Trigger '{trigger_exists[0]}' created.")
        else: print("FAILED: Trigger not found.")

if __name__ == "__main__":
    try:
        run_sql()
    except Exception as e:
        print(f"ERROR: {str(e)}")
