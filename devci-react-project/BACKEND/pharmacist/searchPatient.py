from flask import request, Blueprint, jsonify
import sqlite3

searchPatient_bp = Blueprint('searchpatient', __name__)
@searchPatient_bp.route('/searchpatient', methods=['GET'])
def search_patient():
    patient_name = request.args.get('name')
    
    with sqlite3.connect('pharmacy.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            SELECT patient_name, patient_age, contact, medicine_name, dosage, instructions, doctor_name, status FROM prescriptions WHERE patient_name = ? ORDER BY created_at DESC          
            ''', (patient_name,))
            
            prescriptionInfo = cursor.fetchall()
            
            info = []
            
            for data in prescriptionInfo:
                info.append({
                    'patient_name': data[0],
                    'patient_age': data[1],
                    'contact': data[2],
                    'medicine_name': data[3],
                    'dosage': data[4],
                    'instructions': data[5],
                    'doctor_name': data[6],
                    'status': data[7]
                })
                
            if not info:
                return jsonify({'message': 'No prescription found'}), 404
            
            return jsonify(info), 200
        except sqlite3.Error as e:
            print(str(e))
            return jsonify(str(e)), 500
    

