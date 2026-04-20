import pyodbc

conn_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-F51QMJ8\\SQLEXPRESS;DATABASE=ApartmentDB;Trusted_Connection=yes;Encrypt=no;'
try:
    conn = pyodbc.connect(conn_str, timeout=5)
    print("SUCCESS: Connection to MSSQL established.")
    conn.close()
except Exception as e:
    print(f"FAILED: {str(e)}")
