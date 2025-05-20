from flask import request, Blueprint, jsonify
from database import register_user
import sqlite3
import bcrypt

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/register-doctors', methods=['POST'])
def add_doctor():
    data = request.json
    
    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')
    specialization = data.get('specialization')
    hospital = data.get('hospital')
    
    try:
        register_user(username, password, role='doctor', full_name=full_name, specialization=specialization, hospital=hospital)
        return jsonify({'message': 'Doctor registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
# @admin_bp.route('/admin/doctors', methods=["GET"])
# def get_doctors():
#     with sqlite3.connect('pharmacy.db') as conn:
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#             SELECT u.id, d.full_name, d.specialization, d.hospital
#             FROM doctors d
#             JOIN users u ON d.user_id = u.id
#             ''')
            
#             doctors = []
#             for row in cursor.fetchall():
#                 doctors.append({
#                     'id': row[0],
#                     'full_name': row[1],
#                     'specialization': row[2],
#                     'hospital': row[3]
#                 })
                
#                 return jsonify({'doctors': doctors}), 200
           
#         except sqlite3.Error as e:
#             return jsonify({'error': str(e)}), 500 
        
@admin_bp.route('/pharmacists-audit', methods=['GET'])
def get_pharmacists():
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            SELECT p.medicine_name, p.status, p.updated_at, ph.full_name FROM prescriptions p JOIN pharmacists ph ON p.pharmacist_id = ph.user_id
            ''')
            
            pharmacists = cursor.fetchall()
            
            results = []
            
            for res in pharmacists:
                results.append({
                    'medicineName': res[0],
                    'status': res[1],
                    'upatedAt': res[2],
                    'pharmacist': {
                        'pharmacistName': res[3]
                    }
                })
        
            return jsonify(results), 200
        except sqlite3.Error as e:
            print(str(e))
            return jsonify({'message': 'Error fetching pharmacists'}), 500

@admin_bp.route('/getdoctors', methods=['GET'])
def get_doctors():
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            SELECT * FROM doctors             
            ''')
            
            doctors = cursor.fetchall()
            
            results = []
            
            for res in doctors:
                results.append({
                    'id': res[0],
                    'doctorName': res[1],
                    'specialization': res[2],
                    'hospital': res[3]
                })
                
            return jsonify(results), 200
        except sqlite3.Error as e:
            print(str(e))
            jsonify(str(e)), 500

@admin_bp.route('/editdoctor/<id>', methods=['PUT'])
def edit_doctor(id):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')
    hospital = data.get('hospital')
    specialization = data.get('specialization')
    
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            UPDATE users SET username = ?, password_hash = ? WHERE id = ?               
            ''', (username, hashed_password, id))
            cursor.execute('''
            UPDATE doctors SET full_name = ?, hospital = ?, specialization = ? WHERE user_id = ?
            ''', ( full_name, hospital, specialization, id))
            conn.commit()
            
            return jsonify({'message': 'Doctor updated successfully'}), 200
        except sqlite3.Error as e:
            print(str(e))
            return jsonify(str(e)), 500
    
@admin_bp.route('/deletedoctor/<id>', methods=['DELETE'])
def delete_doctor(id):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            DELETE FROM users WHERE id = ?      
            ''', (id,))
            
            cursor.execute('''
            DELETE FROM doctors WHERE user_id = ?               
            ''', (id,))
            
            conn.commit()
            
            return jsonify({'message': 'User deleted successfully'}), 200
        except sqlite3.Error as e:
            print(str(e))
            return jsonify(str(e)), 500
            