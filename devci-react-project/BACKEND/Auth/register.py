from flask import request, jsonify, session, Blueprint
from database import register_user
import sqlite3

register_bp = Blueprint("register", __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    role = data.get('role')
    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')
    role = data.get('role', 'doctor')
    specialization = data.get('specialization')
    hospital = data.get('hospital')
    
    try:
        if role == 'doctor':
            specialization = data.get('specialization')
            hospital = data.get('hospital')
            register_user(username, password, role, full_name=full_name, specialization=specialization or "", hospital=hospital or "")
        elif role == 'pharmacist':
            license_number = data.get('license_number')
            register_user(username, password, role, full_name=full_name, license_number=license_number)
        elif role == 'admin':
            access_level = data.get('access_level')
            register_user(username, password, role, full_name=full_name, access_level=access_level)
        else:
            return jsonify({'error': 'Invalid role'}), 400
        
        return jsonify({'message': 'User registered successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500