# app.py extension - Add these endpoints to your existing app.py file
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
from database import login, register_user, init_db, add_patient
import os
import secrets
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize the database
init_db()

# Doctor endpoints
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    try:
        with sqlite3.connect('pharmacy.db') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
                SELECT u.id, d.full_name, d.specialization, d.hospital, u.email
                FROM doctors d 
                JOIN users u ON d.user_id = u.id
            """)
            doctors = [dict(row) for row in cursor.fetchall()]
            return jsonify(doctors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctors', methods=['POST'])
def create_doctor():
    data = request.json
    try:
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        specialization = data.get('specialization')
        hospital = data.get('hospital')
        
        register_user(email, password, 'doctor', full_name=full_name, 
                      specialization=specialization, hospital=hospital)
        return jsonify({'message': 'Doctor created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctors/<int:id>', methods=['PUT'])
def update_doctor(id):
    data = request.json
    try:
        with sqlite3.connect('pharmacy.db') as db:
            cursor = db.cursor()
            updates = []
            params = []
            
            if 'full_name' in data:
                updates.append('full_name = ?')
                params.append(data['full_name'])
            
            if 'specialization' in data:
                updates.append('specialization = ?')
                params.append(data['specialization'])
                
            if 'hospital' in data:
                updates.append('hospital = ?')
                params.append(data['hospital'])
                
            if not updates:
                return jsonify({'error': 'No fields to update'}), 400
                
            params.append(id)
            query = f"UPDATE doctors SET {', '.join(updates)} WHERE user_id = ?"
            cursor.execute(query, params)
            
            if cursor.rowcount == 0:
                return jsonify({'error': 'Doctor not found'}), 404
                
            return jsonify({'message': 'Doctor updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctors/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    try:
        with sqlite3.connect('pharmacy.db') as db:
            cursor = db.cursor()
            cursor.execute('DELETE FROM doctors WHERE user_id = ?', (id,))
            cursor.execute('DELETE FROM users WHERE id = ?', (id,))
            
            if cursor.rowcount == 0:
                return jsonify({'error': 'Doctor not found'}), 404
                
            return jsonify({'message': 'Doctor deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Patient endpoints
@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.json
    try:
        full_name = data.get('full_name')
        date_of_birth = data.get('date_of_birth')
        contact_number = data.get('contact_number')
        address = data.get('address')
        medical_history = data.get('medical_history')
        
        add_patient(full_name, date_of_birth, contact_number, address, medical_history)
        return jsonify({'message': 'Patient added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients', methods=['GET'])
def get_patients():
    try:
        with sqlite3.connect('pharmacy.db') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
                SELECT id, full_name, date_of_birth, contact_number, address, medical_history
                FROM patients
            """)
            patients = [dict(row) for row in cursor.fetchall()]
            return jsonify(patients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Prescription endpoints
@app.route('/api/prescriptions', methods=['GET'])
def get_prescriptions():
    try:
        with sqlite3.connect('pharmacy.db') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
                SELECT p.id, p.doctor_id, d.full_name AS doctor_name, 
                       p.patient_id, pt.full_name AS patient_name, 
                       p.medicine_name, p.dosage, p.status, p.created_at
                FROM prescriptions p
                JOIN doctors d ON p.doctor_id = d.user_id
                JOIN patients pt ON p.patient_id = pt.id
            """)
            prescriptions = [dict(row) for row in cursor.fetchall()]
            return jsonify(prescriptions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prescriptions/doctor/<int:doctor_id>', methods=['GET'])
def get_doctor_prescriptions(doctor_id):
    try:
        with sqlite3.connect('pharmacy.db') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
                SELECT p.id, p.doctor_id, d.full_name as doctor_name, 
                       p.patient_id, p.medicine_id, p.dosage, p.status, p.created_at
                FROM prescriptions p
                JOIN doctors d ON p.doctor_id = d.user_id
                WHERE p.doctor_id = ?
            """, (doctor_id,))
            prescriptions = [dict(row) for row in cursor.fetchall()]
            return jsonify(prescriptions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prescriptions', methods=['POST'])
def create_prescription():
    data = request.json
    try:
        doctor_id = data.get('doctor_id')
        patient_id = data.get('patient_id')
        medicine_name = data.get('medicine_name')
        dosage = data.get('dosage')
        
        with sqlite3.connect('pharmacy.db') as db:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO prescriptions 
                (doctor_id, patient_id, medicine_name, dosage, status, created_at)
                VALUES (?, ?, ?, ?, 'pending', ?)
            """, (doctor_id, patient_id, medicine_name, dosage, datetime.now().isoformat()))
            
            return jsonify({'message': 'Prescription created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prescriptions/<int:id>', methods=['PUT'])
def update_prescription(id):
    data = request.json
    try:
        with sqlite3.connect('pharmacy.db') as db:
            cursor = db.cursor()
            updates = []
            params = []
            
            if 'status' in data:
                updates.append('status = ?')
                params.append(data['status'])
                
            if not updates:
                return jsonify({'error': 'No fields to update'}), 400
                
            params.append(id)
            query = f"UPDATE prescriptions SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            
            if cursor.rowcount == 0:
                return jsonify({'error': 'Prescription not found'}), 404
                
            return jsonify({'message': 'Prescription updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Audit log endpoints
@app.route('/api/audit-logs', methods=['GET'])
def get_audit_logs():
    try:
        with sqlite3.connect('pharmacy.db') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
                SELECT id, action, details, created_at
                FROM audit_logs
                ORDER BY created_at DESC
            """)
            logs = [dict(row) for row in cursor.fetchall()]
            return jsonify(logs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audit-logs', methods=['POST'])
def create_audit_log():
    data = request.json
    try:
        action = data.get('action')
        details = data.get('details', '')
        
        with sqlite3.connect('pharmacy.db') as db:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO audit_logs (action, details, created_at)
                VALUES (?, ?, ?)
            """, (action, details, datetime.now().isoformat()))
            
            return jsonify({'message': 'Audit log created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '_main_':
    app.run(debug=True)