from flask import request, jsonify, session, Blueprint, g
import sqlite3
from middleware.role_middleware import role_required

prescription_bp = Blueprint('prescription', __name__)

@prescription_bp.route('/prescriptions', methods=['POST'])
# @role_required('doctor')
def add_prescription():
    data = request.json
    print(data)
    
    doctor_id = data.get('doctorId')
    doctor_Name = data.get("doctorName")
    patient_name = data.get('patientName')
    patient_age = data.get('patientAge')
    contact = data.get('contact')
    medicine_id = data.get('medicineId')
    medicine_name = data.get('medication')
    dosage = data.get('dosage')
    instructioins = data.get('instructions')
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO prescriptions(doctor_id, doctor_name, patient_name, patient_age, contact, medicine_id, medicine_name, dosage, instructions, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
            ''', (doctor_id, doctor_Name, patient_name, patient_age, contact, medicine_id, medicine_name ,dosage, instructioins))
            conn.commit()
            return jsonify({'message': "Prescription recorded successfully", 'id': cursor.lastrowid})
        except sqlite3.Error as e:
            print(str(e))
            return jsonify({'error': str(e)}), 500
        