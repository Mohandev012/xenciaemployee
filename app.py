import logging
logging.basicConfig(filename='flask-error.log', level=logging.DEBUG)
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=tcp:xenserverdb.database.windows.net;'
        'DATABASE=xendb;'
        'UID=sqladmin;'
        'PWD=Xencia@12345;'
        'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    )
    return conn

@app.route('/api/employees/sachin')
def sachin_employees():
    return get_team_employees('sachin team')

@app.route('/api/employees/naveen')
def naveen_employees():
    return get_team_employees('naveen team')

@app.route('/api/employees/anand')
def anand_employees():
    return get_team_employees('anand team')

def get_team_employees(team_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Emp_ID AS EmpID, Name, Designation, Email, Phone, Team
        FROM Employee_Details
        WHERE LOWER(Team) = ?
    """, team_name.lower())
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/sachin')
def sachin():
    return render_template('sachin_employee_details.html')

@app.route('/naveen')
def naveen():
    return render_template('naveen_employee_details.html')

@app.route('/anand')
def anand():
    return render_template('anand_employee_details.html')

if __name__ == '__main__':
    app.run(debug=True)