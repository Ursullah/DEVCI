# This extends your existing app.py file with the required endpoints

from flask import Flask, request, jsonify, request, session
from flask_cors import CORS
import secrets
import sqlite3
from database import login, register_user, init_db, require_role
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
#CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)   
CORS(app, origins='http://localhost:5173', supports_credentials=True, allow_headers=['Content-Type', 'Authorization'])

# Initialize the database
init_db()

# Authentication middleware
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(user, *args, **kwargs)
    return decorated

# Role middleware
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(user, *args, **kwargs):
            if user.get('role') != role:
                return jsonify({'error': f'Access denied. {role} role required'}), 403
            return f(user, *args, **kwargs)
        return decorated
    return decorator

# Existing routes
@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    role = data.get('role')
    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')
    role = data.get('role', 'doctor')
    specialization = data.get('specialization')
    hospital = data.get('hospital')
    
    try:
        if role == 'doctor':
            specialization = data.get('specialization')
            hospital = data.get('hospital')
            register_user(username, password, role, full_name=full_name, specialization=specialization or "", hospital=hospital or "")
        elif role == 'pharmacist':
            license_number = data.get('license_number')
            register_user(username, password, role, full_name=full_name, license_number=license_number)
        elif role == 'admin':
            access_level = data.get('access_level')
            register_user(username, password, role, full_name=full_name, access_level=access_level)
        else:
            return jsonify({'error': 'Invalid role'}), 400
        
        return jsonify({'message': 'User registered successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def user_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = login(username, password)
    if user:
        session['user'] = user
        
        # Get additional user details based on role
        with sqlite3.connect('pharmacy.db') as conn:
            cursor = conn.cursor()
            
            if user['role'] == 'doctor':
                cursor.execute("SELECT full_name, specialization, hospital FROM doctors WHERE user_id = ?", (user['id'],))
                details = cursor.fetchone()
                if details:
                    user['full_name'] = details[0]
                    user['specialization'] = details[1]
                    user['hospital'] = details[2]
            elif user['role'] == 'pharmacist':
                cursor.execute("SELECT full_name, license_number FROM pharmacists WHERE user_id = ?", (user['id'],))
                details = cursor.fetchone()
                if details:
                    user['full_name'] = details[0]
                    user['license_number'] = details[1]
            elif user['role'] == 'admin':
                cursor.execute("SELECT full_name, access_level FROM admins WHERE user_id = ?", (user['id'],))
                details = cursor.fetchone()
                if details:
                    user['full_name'] = details[0]
                    user['access_level'] = details[1]
                    
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'})

@app.route('/user', methods=['GET'])
def get_user():
    user = session.get('user')
    if user:
        return jsonify({'user': user})
    return jsonify({'error': 'Unauthorized'}), 401

# New prescription routes for doctors
@app.route('/prescriptions', methods=['POST'])
# @auth_required
@role_required('doctor')
def create_prescription(user):
    data = request.json
    patient_id = data.get('patient_id')
    medicine_id = data.get('medicine_id')
    dosage = data.get('dosage')
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO prescriptions 
                (doctor_id, patient_id, medicine_id, dosage, status)
                VALUES (?, ?, ?, ?, 'pending')
            ''', (user['id'], patient_id, medicine_id, dosage))
            conn.commit()
            return jsonify({'message': 'Prescription created successfully', 'id': cursor.lastrowid})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

@app.route('/prescriptions/doctor', methods=['GET'])
# @auth_required
@role_required('doctor')
def get_doctor_prescriptions(user):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT 
                    p.id, 
                    u.username as patient_name, 
                    m.name as medicine_name,
                    p.dosage, 
                    p.status, 
                    p.created_at
                FROM prescriptions p
                JOIN users u ON p.patient_id = u.id
                JOIN medicines m ON p.medicine_id = m.id
                WHERE doctor_id = ?
                ORDER BY created_at DESC
            ''', (user['id'],))
            
            prescriptions = []
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                prescriptions.append(dict(zip(columns, row)))
                
            return jsonify({'prescriptions': prescriptions})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

# New prescription routes for pharmacists
@app.route('/prescriptions/verify', methods=['POST'])
# @auth_required
@role_required('pharmacist')
def verify_prescription(user):
    data = request.json
    doctor_name = data.get('doctor_name')
    medication = data.get('medication')
    patient_info = data.get('patient_info', '')
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, specialization FROM doctors 
                WHERE full_name LIKE ? LIMIT 1
            ''', (f'%{doctor_name}%',))
            
            doctor = cursor.fetchone()
            
            if not doctor:
                return jsonify({'status': 'critical', 'message': 'Doctor not found in database'})
                
            doctor_id, specialization = doctor
            
            cursor.execute('''
                SELECT 1 FROM medicines 
                WHERE name = ?
            ''', (medication,))
            
            is_valid = cursor.fetchone() is not None
            status = 'valid' if is_valid else 'warning'
            
            # Log verification
            cursor.execute('''
                INSERT INTO prescriptions 
                (pharmacist_id, doctor_id, medicine_id, patient_id, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (user['id'], doctor_id, medication, patient_info, status))
            
            conn.commit()
            
            result = {
                'status': status,
                'message': 'Verification successful' if is_valid else f'Alert: {medication} may not be typically prescribed by {specialization}s'
            }
            
            return jsonify(result)
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

@app.route('/prescriptions/search/patient', methods=['GET'])
# @auth_required
@role_required('pharmacist')
def search_by_patient(user):
    patient_name = request.args.get('name', '')
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT 
                    p.id,
                    u.username AS patient_name,
                    m.name AS medication,
                    p.dosage,
                    p.status,
                    d.full_name AS doctor_name,
                    d.specialization,
                    p.created_at
                FROM prescriptions p
                JOIN users u ON p.patient_id = u.id
                JOIN medicines m ON p.medicine_id = m.id
                JOIN doctors d ON p.doctor_id = d.user_id
                WHERE u.username LIKE ?
                ORDER BY p.created_at DESC
            ''', (f'%{patient_name}%',))
            
            prescriptions = []
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                prescriptions.append(dict(zip(columns, row)))
                
            return jsonify({'prescriptions': prescriptions})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

@app.route('/prescriptions/search/id/<id>', methods=['GET'])
# @auth_required
@role_required('pharmacist')
def search_by_id(id):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT 
                    p.id,
                    u.username AS patient_name,
                    m.name AS medication,
                    p.dosage,
                    p.status,
                    d.full_name AS doctor_name,
                    d.specialization,
                    p.created_at
                FROM prescriptions p
                JOIN users u ON p.patient_id = u.id
                JOIN medicines m ON p.medicine_id = m.id
                JOIN doctors d ON p.doctor_id = d.user_id
                WHERE p.id = ?
            ''', (id,))
            
            row = cursor.fetchone()
            
            if not row:
                return jsonify({'error': 'Prescription not found'}), 404
                
            columns = [column[0] for column in cursor.description]
            prescription = dict(zip(columns, row))
                
            return jsonify({'prescription': prescription})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

@app.route('/prescriptions/audit', methods=['GET'])
@auth_required
@role_required('pharmacist')
def get_audit_log(user):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT 
                    p.created_at, 
                    m.name as medicine, 
                    p.status 
                FROM prescriptions p
                JOIN medicines m ON p.medicine_id = m.id 
                WHERE pharmacist_id = ?
                ORDER BY created_at DESC LIMIT 10
            ''', (user['id'],))
            
            logs = []
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                logs.append(dict(zip(columns, row)))
                
            return jsonify({'logs': logs})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

# New admin routes
@app.route('/admin/doctors', methods=['GET'])
@auth_required
@role_required('admin')
def get_doctors(user):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT u.id, d.full_name, d.specialization, d.hospital 
                FROM doctors d 
                JOIN users u ON d.user_id = u.id
            """)
            
            doctors = []
            for row in cursor.fetchall():
                doctors.append({
                    'id': row[0],
                    'full_name': row[1],
                    'specialization': row[2],
                    'hospital': row[3]
                })
                
            return jsonify({'doctors': doctors})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

@app.route('/admin/register-doctors', methods=['POST'])
# @auth_required
@role_required('admin')
def add_doctor():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')
    specialization = data.get('specialization')
    hospital = data.get('hospital')
    
    try:
        register_user(username, password, role='doctor', full_name=full_name, 
                     specialization=specialization, hospital=hospital)
        return jsonify({'message': 'Doctor registered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/doctors/<id>', methods=['PUT'])
# @auth_required
@role_required('admin')
def update_doctor(user, id):
    data = request.json
    field = data.get('field')
    value = data.get('value')
    
    valid_fields = ['full_name', 'specialization', 'hospital']
    if field not in valid_fields:
        return jsonify({'error': 'Invalid field'}), 400
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"UPDATE doctors SET {field} = ? WHERE user_id = ?", (value, id))
            conn.commit()
            return jsonify({'message': 'Doctor updated successfully'})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

@app.route('/admin/doctors/<id>', methods=['DELETE'])
# @auth_required
@role_required('admin')
def delete_doctor(user, id):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM doctors WHERE user_id = ?', (id,))
            cursor.execute('DELETE FROM users WHERE id = ?', (id,))
            conn.commit()
            return jsonify({'message': 'Doctor deleted successfully'})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
@app.route('/api/audit-logs', methods=['GET'])
@auth_required
@role_required('pharmacist')
def get_audit_logs(user):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT 
                    p.created_at, 
                    m.name as medicine, 
                    p.status 
                FROM prescriptions p
                JOIN medicines m ON p.medicine_id = m.id 
                WHERE pharmacist_id = ?
                ORDER BY created_at DESC LIMIT 10
            ''', (user['id'],))

            logs = []
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                logs.append(dict(zip(columns, row)))

            return jsonify({'logs': logs})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

# Add endpoint to get medicines
@app.route('/medicines', methods=['GET'])
# @auth_required
def get_medicines(user):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, price, stock, expiry_date FROM medicines")
            
            medicines = []
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                medicines.append(dict(zip(columns, row)))
                
            return jsonify({'medicines': medicines})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

# Add endpoint to get patients
@app.route('/patients', methods=['GET'])
# @auth_required
def get_patients(user):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, username FROM users WHERE role = 'patient'")
            
            patients = []
            for row in cursor.fetchall():
                patients.append({
                    'id': row[0],
                    'username': row[1]
                })
                
            return jsonify({'patients': patients})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)