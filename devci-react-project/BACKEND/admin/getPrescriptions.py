from flask import request, jsonify, Blueprint
import sqlite3

getPrescriptioon_bd = Blueprint('admin_prescription', __name__)

@getPrescriptioon_bd.route('/adminprescription', methods=['GET'])
def get_doctor_prescrition():
    with sqlite3.connect('pharmacy.db') as conn:
        conn.row_factory = sqlite3.Row  # This allows column name access
        cursor = conn.cursor()
        
        try:
            # Explicitly select columns in the correct order
            cursor.execute('''
                SELECT 
                    p.doctor_name,
                    p.patient_name,
                    p.patient_age,
                    p.contact,
                    p.medicine_name,
                    p.dosage,
                    p.instructions,
                    p.status,
                    p.updated_at,
                    ph.full_name AS pharmacist_name
                FROM prescriptions p
                LEFT JOIN pharmacists ph ON p.pharmacist_id = ph.user_id
                ORDER BY p.updated_at DESC
            ''')
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'doctor_name': row['doctor_name'],
                    'patient_name': row['patient_name'],
                    'patient_age': row['patient_age'],
                    'contact': row['contact'],
                    'medicine_name': row['medicine_name'],
                    'dosage': row['dosage'],
                    'instructions': row['instructions'],
                    'status': row['status'],
                    'updated_at': row['updated_at'],
                    'pharmacist': {
                        'pharmacistName': row['pharmacist_name'] if row['pharmacist_name'] else "Unassigned"
                    }
                })
            
            return jsonify(results), 200
            
        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return jsonify({'error': str(e)}), 500