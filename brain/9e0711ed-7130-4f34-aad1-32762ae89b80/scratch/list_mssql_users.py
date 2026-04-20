import pyodbc

conn_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-F51QMJ8\\SQLEXPRESS;DATABASE=ApartmentDB;Trusted_Connection=yes;Encrypt=no;'
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("--- MSSQL Users ---")
    cursor.execute("SELECT username, email FROM auth_user")
    for row in cursor.fetchall():
        print(f"Username: {row.username}, Email: {row.email}")
    conn.close()
except Exception as e:
    print(f"FAILED: {str(e)}")
