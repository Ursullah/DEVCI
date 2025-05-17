from flask import jsonify, request, Blueprint
import sqlite3

verifyPrescription_bp = Blueprint('verifyPrescription', __name__)

@verifyPrescription_bp.route('/verifyprescription', methods=['POST'])
def verify_prescriptioin():
    data = request.json
    
    doctor_name = data.get('doctorName')
    medicine_name = data.get('medicineName')
    patient_name = data.get('patientName')
    
    with sqlite3.connect('pharmacy.db') as conn:
        cusor = conn.cursor()
        
        try:
            cusor.execute('''
            SELECT doctor_name, medicine_name, patient_name FROM prescriptions WHERE patient_name = ? AND doctor_name = ? AND medicine_name = ?
            ''', (patient_name, doctor_name, medicine_name))
            
            prescription = cusor.fetchone()
            
            results = []
            
            for res in prescription:
                results.append({
                    'doctor_name': res[0],
                    'medicine_name': res[1],
                    'patient_name': res[2]
                })
            
            print(results)
                        
            if not prescription:
                return jsonify({'message': 'Prescription no found'}), 404
            
            if prescription:
                cusor.execute('''
                UPDATE prescriptions SET status = 'filled' WHERE patient_name = ?              
                ''', (patient_name,))
                
                conn.commit()
                # conn.close()
                
                return jsonify({'message': 'Prescription verified successfully'})
            
            return results      
        except sqlite3.Error as e:
            print(str(e))
            return jsonify(str(e)), 500
            
            
            
        