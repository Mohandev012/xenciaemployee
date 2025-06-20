import logging
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_cors import CORS
import pyodbc

# Initialize logging and app
logging.basicConfig(filename='flask-error.log', level=logging.DEBUG)
app = Flask(__name__)
CORS(app)
app.secret_key = 'your-secret-key-here'  # Replace with a strong secret

# Database connection
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

# ?? Sachin Login Route
@app.route('/sachin_login', methods=['GET', 'POST'])
def sachin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Login_Credentials WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('sachin'))
        return render_template('sachin_login.html', error='Invalid credentials')
    return render_template('sachin_login.html')

@app.route('/sachin_logout')
def sachin_logout():
    session.clear()
    return redirect(url_for('sachin_login'))

@app.route('/sachin')
def sachin():
    if not session.get('logged_in'):
        return redirect(url_for('sachin_login'))
    return render_template('sachin_employee_details.html')

@app.route('/api/employees/sachin')
def sachin_employees():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    return get_team_employees('sachin team')


# ?? Naveen Login Route
@app.route('/naveen_login', methods=['GET', 'POST'])
def naveen_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Login_Credentials WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('naveen_protected'))
        return render_template('naveen_login.html', error='Invalid credentials')
    return render_template('naveen_login.html')

@app.route('/naveen_logout')
def naveen_logout():
    session.clear()
    return redirect(url_for('naveen_login'))

@app.route('/naveen')
def naveen_protected():
    if not session.get('logged_in'):
        return redirect(url_for('naveen_login'))
    return render_template('naveen_employee_details.html')

@app.route('/api/employees/naveen')
def naveen_employees():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    return get_team_employees('naveen team')


# ?? anand Login Route
@app.route('/anand_login', methods=['GET', 'POST'])
def anand_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Login_Credentials WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('anand_protected'))
        return render_template('anand_login.html', error='Invalid credentials')
    return render_template('anand_login.html')

@app.route('/anand_logout')
def anand_logout():
    session.clear()
    return redirect(url_for('anand_login'))

@app.route('/anand')
def anand_protected():
    if not session.get('logged_in'):
        return redirect(url_for('anand_login'))
    return render_template('anand_employee_details.html')

@app.route('/api/employees/anand')
def anand_employees():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    return get_team_employees('anand team')


# Utility to fetch team employees
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
    
@app.route('/api/certifications/sachin')
def sachin_certifications():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.EmpID, c.Name, c.Certificate, c.Status, c.ExpireDate, c.MailID, c.MS_Link_To_Renew_Cert
        FROM certification_details c
        INNER JOIN Employee_Details e ON c.EmpID = e.Emp_ID
        WHERE LOWER(e.Team) LIKE ?
    """, ('%sachin%',))  # Match team name flexibly

    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(results)
    
@app.route('/api/certifications/naveen')
def naveen_certifications():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.EmpID, c.Name, c.Certificate, c.Status, c.ExpireDate, c.MailID, c.MS_Link_To_Renew_Cert
        FROM certification_details c
        INNER JOIN Employee_Details e ON c.EmpID = e.Emp_ID
        WHERE LOWER(e.Team) LIKE ?
    """, ('%naveen%',))  # Match team name flexibly

    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/api/certifications/anand')
def anand_certifications():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.EmpID, c.Name, c.Certificate, c.Status, c.ExpireDate, c.MailID, c.MS_Link_To_Renew_Cert
        FROM certification_details c
        INNER JOIN Employee_Details e ON c.EmpID = e.Emp_ID
        WHERE LOWER(e.Team) LIKE ?
    """, ('%anand%',))  # Match team name flexibly

    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/api/sops/sachin')
def sachin_sops():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.Engineer, s.Trainee, s.Sr_Engineer, s.SOP_Document, s.Status, s.KT_Session_To_Team
        FROM sops_documents s
        INNER JOIN Employee_Details e ON LOWER(s.Engineer) = LOWER(e.Name) OR LOWER(s.Trainee) = LOWER(e.Name)
        WHERE LOWER(e.Team) = ?
    """, ('sachin team',))
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/api/sops/naveen')
def naveen_sops():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.Engineer, s.Trainee, s.Sr_Engineer, s.SOP_Document, s.Status, s.KT_Session_To_Team
        FROM sops_documents s
        INNER JOIN Employee_Details e ON LOWER(s.Engineer) = LOWER(e.Name) OR LOWER(s.Trainee) = LOWER(e.Name)
        WHERE LOWER(e.Team) = ?
    """, ('naveen team',))
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(results)
    
@app.route('/api/sops/anand')
def anand_sops():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.Engineer, s.Trainee, s.Sr_Engineer, s.SOP_Document, s.Status, s.KT_Session_To_Team
        FROM sops_documents s
        INNER JOIN Employee_Details e ON LOWER(s.Engineer) = LOWER(e.Name) OR LOWER(s.Trainee) = LOWER(e.Name)
        WHERE LOWER(e.Team) = ?
    """, ('anand team',))
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/api/leaves/sachin')
def sachin_leaves():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.Name, l.Leave_Type, l.Leaves_Taken, l.Leave_Pending, l.Remarks
        FROM Employee_Leave_Details l
        INNER JOIN Employee_Details e ON LOWER(e.Name) = LOWER(l.Name)
        WHERE LOWER(e.Team) = 'sachin team'
    """)
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/api/leaves/naveen')
def naveen_leaves():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.Name, l.Leave_Type, l.Leaves_Taken, l.Leave_Pending, l.Remarks
        FROM Employee_Leave_Details l
        INNER JOIN Employee_Details e ON LOWER(e.Name) = LOWER(l.Name)
        WHERE LOWER(e.Team) = 'naveen team'
    """)
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/api/leaves/anand')
def anand_leaves():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.Name, l.Leave_Type, l.Leaves_Taken, l.Leave_Pending, l.Remarks
        FROM Employee_Leave_Details l
        INNER JOIN Employee_Details e ON LOWER(e.Name) = LOWER(l.Name)
        WHERE LOWER(e.Team) = 'anand team'
    """)
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(results)

# ?? Homepage
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
