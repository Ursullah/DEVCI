from flask import request, jsonify, Blueprint
import sqlite3

getPrescriptioon_bd = Blueprint('admin_prescription', __name__)

@getPrescriptioon_bd.route('/adminprescription', methods=['GET'])
def get_doctor_prescrition():    
        
    with sqlite3.connect('pharmacy.db') as conn:
        cusor = conn.cursor()
        
        try:
            cusor.execute('''
            SELECT doctor_name, patient_name, patient_age, contact, medicine_name, dosage, instructions, status FROM prescriptions ORDER BY created_at DESC
            ''')
            
            prescriptions = cusor.fetchall()
            
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