from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret_key_123"

# ===================== DB CONNECTION =====================
def get_db_connection():
    connection = pymysql.connect(
        host='Shital',
        user='vivek',
        password='kavita342005$',  # your MySQL password
        db='hospital1_db',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# ===================== UPLOAD CONFIG =====================
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ===================== ROUTES =====================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cur.fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['role'] = user['role']
            session['doctor_id'] = user.get('id', 1)  # store doctor_id if exists

            if user['role'] == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            elif user['role'] == 'owner':
                return redirect(url_for('owner_dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/doctor-dashboard', methods=['GET', 'POST'])
def doctor_dashboard():
    if 'role' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))

    search = request.args.get('search', '')
    conn = get_db_connection()
    with conn.cursor() as cur:
        if search:
            cur.execute("""
                SELECT * FROM patients 
                WHERE name LIKE %s OR id LIKE %s
            """, ('%' + search + '%', '%' + search + '%'))
        else:
            cur.execute("SELECT * FROM patients")
        patients = cur.fetchall()
    conn.close()

    return render_template('doctor_dashboard.html', patients=patients, doctor_name=session['username'], search=search)

# ===================== PATIENT HISTORY =====================
@app.route('/patient/<int:patient_id>/history', methods=['GET', 'POST'])
def patient_history(patient_id):
    if 'role' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, age, blood_group, admitted_date, discharge_date, diagnosis, photo 
            FROM patients WHERE id = %s
        """, (patient_id,))
        patient = cur.fetchone()

        cur.execute("SELECT MAX(appointment_date) AS last_appointment FROM appointments WHERE patient_id = %s", (patient_id,))
        row = cur.fetchone()
        last_appointment = row['last_appointment'] if row else None

        cur.execute("""
            SELECT date, prescription_details 
            FROM prescriptions WHERE patient_id = %s 
            ORDER BY date DESC
        """, (patient_id,))
        prescriptions = cur.fetchall()
    conn.close()

    if request.method == 'POST':
        new_prescription = request.form.get('prescription')
        new_appointment = request.form.get('appointment_date')
        photo_file = request.files.get('photo')
        doctor_id = session.get('doctor_id', 1)

        conn = get_db_connection()
        with conn.cursor() as cur:
            # ✅ Handle photo upload
            if photo_file and allowed_file(photo_file.filename):
                filename = secure_filename(photo_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # ensure folder exists
                photo_file.save(filepath)
                cur.execute("UPDATE patients SET photo = %s WHERE id = %s", (filename, patient_id))

            # ✅ Add new prescription
            if new_prescription:
                cur.execute("""
                    INSERT INTO prescriptions (patient_id, doctor_id, date, prescription_details)
                    VALUES (%s, %s, %s, %s)
                """, (patient_id, doctor_id, datetime.now().date(), new_prescription))

            # ✅ Add new appointment
            if new_appointment:
                cur.execute("""
                    INSERT INTO appointments (patient_id, doctor_id, appointment_date)
                    VALUES (%s, %s, %s)
                """, (patient_id, doctor_id, new_appointment))

            conn.commit()
        conn.close()

        return redirect(url_for('patient_history', patient_id=patient_id))

    return render_template(
        'patient_history.html',
        patient=patient,
        last_appointment=last_appointment,
        prescriptions=prescriptions
    )

# ===================== OWNER DASHBOARD =====================
@app.route('/owner-dashboard')
def owner_dashboard():
    if 'role' in session and session['role'] == 'owner':
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Total counts
            cur.execute("SELECT COUNT(*) AS total FROM patients")
            total_patients = cur.fetchone()['total']

            cur.execute("SELECT COUNT(*) AS total FROM users WHERE role='doctor'")
            total_doctors = cur.fetchone()['total']

            # Fetch patient list
            cur.execute("SELECT id, name, admitted_date, discharge_date, diagnosis FROM patients")
            patients = cur.fetchall()

            # Fetch doctor list with patient count
            cur.execute("""
                SELECT u.id, u.username, COUNT(p.id) AS total_patients
                FROM users u
                LEFT JOIN prescriptions p ON u.id = p.doctor_id
                WHERE u.role = 'doctor'
                GROUP BY u.id, u.username
            """)
            doctors = cur.fetchall()

        conn.close()

        return render_template(
            'owner_dashboard.html',
            owner_name=session['username'],
            total_patients=total_patients,
            total_doctors=total_doctors,
            admitted_patients=36,
            monthly_revenue=2000000,
            patients=patients,
            doctors=doctors
        )
    else:
        return redirect(url_for('login'))

@app.route('/reports')
def reports():
    if 'role' not in session or session['role'] != 'owner':
        return redirect(url_for('login'))

    conn = get_db_connection()
    with conn.cursor() as cur:
        # --- Monthly Patient Admissions ---
        cur.execute("""
            SELECT 
                DATE_FORMAT(admitted_date, '%%b') AS month, 
                COUNT(*) AS total_admissions
            FROM patients
            WHERE admitted_date IS NOT NULL
            GROUP BY DATE_FORMAT(admitted_date, '%%b')
            ORDER BY MIN(admitted_date)
        """)
        admissions = cur.fetchall()
        months = [row['month'] for row in admissions]
        total_admissions = [row['total_admissions'] for row in admissions]

        # --- Doctor Performance ---
        cur.execute("""
            SELECT u.username AS doctor, COUNT(p.id) AS prescriptions
            FROM prescriptions p
            JOIN users u ON p.doctor_id = u.id
            GROUP BY u.username
        """)
        doctors = cur.fetchall()
        doctor_names = [row['doctor'] for row in doctors]
        doctor_prescriptions = [row['prescriptions'] for row in doctors]

        # --- Monthly Revenue ---
        cur.execute("""
            SELECT 
                DATE_FORMAT(payment_date, '%%b') AS month, 
                SUM(amount) AS total_revenue
            FROM payments
            WHERE payment_date IS NOT NULL
            GROUP BY DATE_FORMAT(payment_date, '%%b')
            ORDER BY MIN(payment_date)
        """)
        revenue = cur.fetchall()
        rev_months = [row['month'] for row in revenue]
        rev_amounts = [row['total_revenue'] for row in revenue]

    conn.close()

    return render_template(
        'reports.html',
        months=months,
        total_admissions=total_admissions,
        doctor_names=doctor_names,
        doctor_prescriptions=doctor_prescriptions,
        rev_months=rev_months,
        rev_amounts=rev_amounts
    )



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

    ...

# ===================== MAIN =====================
@app.route('/discharge/<int:patient_id>', methods=['GET'])
def discharge_patient(patient_id):
    if 'role' not in session or session['role'] != 'doctor':
        return redirect(url_for('login'))

    conn = get_db_connection()
    with conn.cursor() as cur:
        # Update discharge_date
        cur.execute("""
            UPDATE patients
            SET discharge_date = CURDATE()
            WHERE id = %s
        """, (patient_id,))

        # Calculate total payments
        cur.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total_bill
            FROM payments
            WHERE patient_id = %s
        """, (patient_id,))
        total = cur.fetchone()['total_bill']

        # Insert into discharge_summary
        cur.execute("""
            INSERT INTO discharge_summary (patient_id, discharge_date, total_bill, summary_notes)
            VALUES (%s, CURDATE(), %s, %s)
        """, (patient_id, total, 'Patient discharged successfully.'))

        # Fetch patient info and payments
        cur.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        patient = cur.fetchone()

        cur.execute("""
            SELECT * FROM payments
            WHERE patient_id = %s
            ORDER BY payment_date DESC
        """, (patient_id,))
        payments = cur.fetchall()

        conn.commit()
    conn.close()

    return render_template(
        'discharge_summary.html',
        patient=patient,
        payments=payments,
        total=total
    )
@app.route('/add-doctor', methods=['POST'])
def add_doctor():
    if 'role' not in session or session['role'] != 'owner':
        return redirect(url_for('login'))

    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, 'doctor')",
                (username, password)
            )
            conn.commit()
        conn.close()

    return redirect(url_for('owner_dashboard'))

# ===================== REPORTING & ANALYTICS =====================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
