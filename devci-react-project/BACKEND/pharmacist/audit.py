from flask import Blueprint, jsonify
import sqlite3

audit_bp = Blueprint('audit', __name__)
@audit_bp.route('/audit', methods=['GET'])
def audit():
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            SELECT doctor_name, patient_name, medicine_name, dosage, instructions, status FROM prescriptions               
            ''')
            
            audit = cursor.fetchall()
            
            results = []
            
            for res in audit:
                results.append({
                    'doctorName': res[0],
                    'patientName': res[1],
                    'medicineName': res[2],
                    'dosage': res[3],
                    'instructions': res[4],
                    'status': res[5]
                })
                
            return results
        except sqlite3.Error as e:
            print(str(e))
            return jsonify(str(e))