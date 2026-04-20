from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False 

CONN_STR = 'Driver={ODBC Driver 17 for SQL Server};Server=.\\SQLEXPRESS;Database=ApartmentDB;Trusted_Connection=yes;'

def query(sql):
    with pyodbc.connect(CONN_STR) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        cols = [c[0] for c in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]

@app.route('/api/data')
def get_data():
    return jsonify({
        "tenants": query("SELECT * FROM Tenants"),
        "rooms": query("SELECT * FROM Rooms"),
        "invoices": query("SELECT * FROM Invoices"),
        "repairs": query("SELECT * FROM Repairs")
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)