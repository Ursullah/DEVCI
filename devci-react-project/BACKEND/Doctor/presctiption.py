from flask import request, jsonify, session, Blueprint, g
import sqlite3
from middleware.role_middleware import role_required

prescription_bp = Blueprint('prescription', __name__)

@prescription_bp.route('/prescriptions', methods=['POST'])
# @role_required('doctor')
def add_prescription():
    data = request.json
    print(data)
    # doctor = g.user

    # if not doctor:
    #     return jsonify({'error': 'unauthorized'}), 401
    
    patient_id = data.get('patient_id')
    medicine_id = data.get('medicine_id')
    doctor_id = data.get('doctorId')
    dosage = data.get('dosage')
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO prescriptions(doctor_id, patient_id, medicine_id, dosage, status) VALUES (?, ?, ?, ?. 'pending')
            ''', (doctor_id, patient_id, medicine_id,dosage))
            conn.commit()
            return jsonify({'message': "Prescription recorded successfully", 'id': cursor.lastrowid})
        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        