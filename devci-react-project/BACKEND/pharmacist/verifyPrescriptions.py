from flask import jsonify, request, Blueprint
import sqlite3

verifyPrescription_bp = Blueprint('verifyPrescription', __name__)

@verifyPrescription_bp.route('/verifyprescription', methods=['POST'])
def verify_prescription():  
    data = request.json
    
    doctor_name = data.get('doctorName')
    medicine_name = data.get('medicineName')
    patient_name = data.get('patientName')
    pharmacist_id = data.get('pharmacistId')
    
    print(pharmacist_id)
    
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()  
        
        try:
            cursor.execute('''
                SELECT doctor_name, medicine_name, patient_name 
                FROM prescriptions 
                WHERE patient_name = ? AND medicine_name = ? AND doctor_name = ?
            ''', (patient_name, medicine_name, doctor_name))
            
            prescription = cursor.fetchone()
            
            if not prescription:
                return jsonify({'message': 'Prescription not found'}), 404
            
            cursor.execute('''
                UPDATE prescriptions 
                SET pharmacist_id = ?, 
                    status = 'filled', 
                    updated_at = CURRENT_TIMESTAMP
                WHERE patient_name = ? AND doctor_name = ? AND medicine_name = ?            
            ''', (pharmacist_id, patient_name, doctor_name, medicine_name))
            
            conn.commit()
            
            return jsonify({
                'message': 'Prescription verified successfully',
                'data': {
                    'doctorName': prescription[0],
                    'medicineName': prescription[1],
                    'patientName': prescription[2]
                }
            })
            
        except sqlite3.Error as e:
            print(str(e))
            return jsonify({'message': str(e)}), 500