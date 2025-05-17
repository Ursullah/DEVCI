from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token
from database import login
import sqlite3
login_bp = Blueprint("login", __name__)

@login_bp.route('/login', methods=['POST'])
def user_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = login(username, password)
    if user:
        session['user'] = user
        
        # Get additional user details based on role
        with sqlite3.connect('pharmacy.db') as conn:
            cursor = conn.cursor()
            
            if user['role'] == 'doctor':
                cursor.execute("SELECT full_name, specialization, hospital FROM doctors WHERE user_id = ?", (user['id'],))
                details = cursor.fetchone()
                if details:
                    user['full_name'] = details[0]
                    user['specialization'] = details[1]
                    user['hospital'] = details[2]
            elif user['role'] == 'pharmacist':
                cursor.execute("SELECT full_name, license_number FROM pharmacists WHERE user_id = ?", (user['id'],))
                details = cursor.fetchone()
                if details:
                    user['full_name'] = details[0]
                    user['license_number'] = details[1]
            elif user['role'] == 'admin':
                cursor.execute("SELECT full_name, access_level FROM admins WHERE user_id = ?", (user['id'],))
                details = cursor.fetchone()
                if details:
                    user['full_name'] = details[0]
                    user['access_level'] = details[1]
                    
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401