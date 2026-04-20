import pyodbc

# Connect to the database
conn_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-F51QMJ8\\SQLEXPRESS;DATABASE=ApartmentDB;Trusted_Connection=yes;Encrypt=no;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Check current structure
cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'django_migrations'")
for row in cursor.fetchall():
    print(row)

# Alter the column
try:
    cursor.execute("ALTER TABLE django_migrations ALTER COLUMN applied datetime2;")
    conn.commit()
    print("Altered applied column to datetime2")
except Exception as e:
    print(f"Error: {e}")

cursor.close()
conn.close()