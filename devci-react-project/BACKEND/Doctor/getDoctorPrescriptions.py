from flask import request, jsonify, Blueprint
import sqlite3

doctorPrescriptioon_bd = Blueprint('doctor_prescription', __name__)

@doctorPrescriptioon_bd.route('/doctorprescription', methods=['GET'])
def get_doctor_prescrition():    
    doctor_id = request.args.get('id')
    
    if not doctor_id:
        return jsonify({'error': 'Doctor ID is required'})
    
    with sqlite3.connect('pharmacy.db') as conn:
        cusor = conn.cursor()
        
        try:
            cusor.execute('''
            SELECT doctor_name, patient_name, patient_age, contact, medicine_name, dosage, instructions, status FROM prescriptions WHERE doctor_id = ? ORDER BY created_at DESC
            ''', (doctor_id,))
            
            prescriptions = cusor.fetchall()
            
            # results = [dict(row) for row in prescriptions]
            results = []
            
            for pres in prescriptions:
                results.append({
                    'doctor_name': pres[0],
                    'patient_name': pres[1],
                    'patient_age': pres[2],
                    'contact': pres[3],
                    'medicine_name': pres[4],
                    'dosage': pres[5],
                    'instruction': pres[6],
                    'status': pres[7]
                })
            
            return results
        except sqlite3.Error as e:
            print(str(e))
            return jsonify(str(e))