# This extends your existing app.py file with the required endpoints

from flask import Flask, request, jsonify, request, session
from flask_cors import CORS
import secrets
import sqlite3
from database import login, register_user, init_db, require_role
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

from Auth.login import login_bp
from Auth.register import register_bp
from Doctor.presctiption import prescription_bp
from medicine.medicine import medicine_bp
from medicine.addMedicine import add_medicine_bp
from admin.admin import admin_bp
from Doctor.getDoctorPrescriptions import doctorPrescriptioon_bd
from pharmacist.searchPatient import searchPatient_bp
from pharmacist.verifyPrescriptions import verifyPrescription_bp
from pharmacist.audit import audit_bp

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pharmacy.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)   
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})
# Initialize the database
init_db = SQLAlchemy(app)

app.register_blueprint(login_bp, url_prefix='/api')
app.register_blueprint(register_bp, url_prefix='/api')
app.register_blueprint(prescription_bp, url_prefix='/api')
app.register_blueprint(medicine_bp, url_prefix='/api')
app.register_blueprint(add_medicine_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(doctorPrescriptioon_bd, url_prefix='/api')
app.register_blueprint(searchPatient_bp, url_prefix='/api')
app.register_blueprint(verifyPrescription_bp, url_prefix='/api')
app.register_blueprint(audit_bp, url_prefix='/api')



# Authentication middleware
#
   #

# Existing routes
@app.route('/test')
def home():
    return "Flask server is running!"



@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'})

# @app.route('/user', methods=['GET'])
# def get_user():
#     user = session.get('user')
#     if user:
#         return jsonify({'user': user})
#     return jsonify({'error': 'Unauthorized'}), 401



# @app.route('/prescriptions/search/patient', methods=['GET'])
# # @auth_required
# @role_required('pharmacist')
# def search_by_patient(user):
#     patient_name = request.args.get('name', '')
    
#     with sqlite3.connect('pharmacy.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 SELECT 
#                     p.id,
#                     u.username AS patient_name,
#                     m.name AS medication,
#                     p.dosage,
#                     p.status,
#                     d.full_name AS doctor_name,
#                     d.specialization,
#                     p.created_at
#                 FROM prescriptions p
#                 JOIN users u ON p.patient_id = u.id
#                 JOIN medicines m ON p.medicine_id = m.id
#                 JOIN doctors d ON p.doctor_id = d.user_id
#                 WHERE u.username LIKE ?
#                 ORDER BY p.created_at DESC
#             ''', (f'%{patient_name}%',))
            
#             prescriptions = []
#             columns = [column[0] for column in cursor.description]
#             for row in cursor.fetchall():
#                 prescriptions.append(dict(zip(columns, row)))
                
#             return jsonify({'prescriptions': prescriptions})
#         except sqlite3.Error as e:
#             return jsonify({'error': str(e)}), 500

# @app.route('/prescriptions/search/id/<id>', methods=['GET'])
# # @auth_required
# @role_required('pharmacist')
# def search_by_id(id):
#     with sqlite3.connect('pharmacy.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 SELECT 
#                     p.id,
#                     u.username AS patient_name,
#                     m.name AS medication,
#                     p.dosage,
#                     p.status,
#                     d.full_name AS doctor_name,
#                     d.specialization,
#                     p.created_at
#                 FROM prescriptions p
#                 JOIN users u ON p.patient_id = u.id
#                 JOIN medicines m ON p.medicine_id = m.id
#                 JOIN doctors d ON p.doctor_id = d.user_id
#                 WHERE p.id = ?
#             ''', (id,))
            
#             row = cursor.fetchone()
            
#             if not row:
#                 return jsonify({'error': 'Prescription not found'}), 404
                
#             columns = [column[0] for column in cursor.description]
#             prescription = dict(zip(columns, row))
                
#             return jsonify({'prescription': prescription})
#         except sqlite3.Error as e:
#             return jsonify({'error': str(e)}), 500

# @app.route('/prescriptions/audit', methods=['GET'])
# #
# @role_required('pharmacist')
# def get_audit_log(user):
#     with sqlite3.connect('pharmacy.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 SELECT 
#                     p.created_at, 
#                     m.name as medicine, 
#                     p.status 
#                 FROM prescriptions p
#                 JOIN medicines m ON p.medicine_id = m.id 
#                 WHERE pharmacist_id = ?
#                 ORDER BY created_at DESC LIMIT 10
#             ''', (user['id'],))
            
#             logs = []
#             columns = [column[0] for column in cursor.description]
#             for row in cursor.fetchall():
#                 logs.append(dict(zip(columns, row)))
                
#             return jsonify({'logs': logs})
#         except sqlite3.Error as e:
#             return jsonify({'error': str(e)}), 500

# # New admin routes
# @app.route('/admin/doctors', methods=['GET'])
# #
# @role_required('admin')
# def get_doctors(user):
#     with sqlite3.connect('pharmacy.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute("""
#                 SELECT u.id, d.full_name, d.specialization, d.hospital 
#                 FROM doctors d 
#                 JOIN users u ON d.user_id = u.id
#             """)
            
#             doctors = []
#             for row in cursor.fetchall():
#                 doctors.append({
#                     'id': row[0],
#                     'full_name': row[1],
#                     'specialization': row[2],
#                     'hospital': row[3]
#                 })
                
#             return jsonify({'doctors': doctors})
#         except sqlite3.Error as e:
#             return jsonify({'error': str(e)}), 500

# @app.route('/admin/register-doctors', methods=['POST'])
# # @auth_required
# @role_required('admin')
# def add_doctor():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')
#     full_name = data.get('full_name')
#     specialization = data.get('specialization')
#     hospital = data.get('hospital')
    
#     try:
#         register_user(username, password, role='doctor', full_name=full_name, 
#                      specialization=specialization, hospital=hospital)
#         return jsonify({'message': 'Doctor registered successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/admin/doctors/<id>', methods=['PUT'])
# # @auth_required
# @role_required('admin')
# def update_doctor(user, id):
#     data = request.json
#     field = data.get('field')
#     value = data.get('value')
    
#     valid_fields = ['full_name', 'specialization', 'hospital']
#     if field not in valid_fields:
#         return jsonify({'error': 'Invalid field'}), 400
    
#     with sqlite3.connect('pharmacy.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute(f"UPDATE doctors SET {field} = ? WHERE user_id = ?", (value, id))
#             conn.commit()
#             return jsonify({'message': 'Doctor updated successfully'})
#         except sqlite3.Error as e:
#             return jsonify({'error': str(e)}), 500

# @app.route('/admin/doctors/<id>', methods=['DELETE'])
# # @auth_required
# @role_required('admin')
# def delete_doctor(user, id):
#     with sqlite3.connect('pharmacy.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute('DELETE FROM doctors WHERE user_id = ?', (id,))
#             cursor.execute('DELETE FROM users WHERE id = ?', (id,))
#             conn.commit()
#             return jsonify({'message': 'Doctor deleted successfully'})
#         except sqlite3.Error as e:
#             return jsonify({'error': str(e)}), 500
# @app.route('/api/audit-logs', methods=['GET'])
# #
# @role_required('pharmacist')
# def get_audit_logs(user):
#     with sqlite3.connect('pharmacy.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 SELECT 
#                     p.created_at, 
#                     m.name as medicine, 
#                     p.status 
#                 FROM prescriptions p
#                 JOIN medicines m ON p.medicine_id = m.id 
#                 WHERE pharmacist_id = ?
#                 ORDER BY created_at DESC LIMIT 10
#             ''', (user['id'],))

#             logs = []
#             columns = [column[0] for column in cursor.description]
#             for row in cursor.fetchall():
#                 logs.append(dict(zip(columns, row)))

#             return jsonify({'logs': logs})
#         except sqlite3.Error as e:
#             return jsonify({'error': str(e)}), 500

# # Add endpoint to get medicines
# @app.route('/medicines', methods=['GET'])
# # @auth_required
# def get_medicines(user):
#     with sqlite3.connect('pharmacy.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute("SELECT id, name, price, stock, expiry_date FROM medicines")
            
#             medicines = []
#             columns = [column[0] for column in cursor.description]
#             for row in cursor.fetchall():
#                 medicines.append(dict(zip(columns, row)))
                
#             return jsonify({'medicines': medicines})
#         except sqlite3.Error as e:
#             return jsonify({'error': str(e)}), 500

# # Add endpoint to get patients
# @app.route('/patients', methods=['GET'])
# # @auth_required
# def get_patients(user):
#     with sqlite3.connect('pharmacy.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute("SELECT id, username FROM users WHERE role = 'patient'")
            
#             patients = []
#             for row in cursor.fetchall():
#                 patients.append({
#                     'id': row[0],
#                     'username': row[1]
#                 })
                
#             return jsonify({'patients': patients})
#         except sqlite3.Error as e:
#             return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)