from flask import request, Blueprint, jsonify
from database import register_user
import sqlite3

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/register-doctors', methods=['POST'])
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
    
    
@admin_bp.route('/admin/doctors', methods=["GET"])
def get_doctors():
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            SELECT u.id, d.full_name, d.specialization, d.hospital
            FROM doctors d
            JOIN users u ON d.user_id = u.id
            ''')
            
            doctors = []
            for row in cursor.fetchall():
                doctors.append({
                    'id': row[0],
                    'full_name': row[1],
                    'specialization': row[2],
                    'hospital': row[3]
                })
                
                return jsonify({'doctors': doctors}), 200
           
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500 