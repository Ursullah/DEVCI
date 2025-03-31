from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity
from auth import jwt, role_required
from database import init_db, register_user, login
import sqlite3

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your-ultra-secure-key"
jwt.init_app(app)
init_db()

# ------------------- Auth -------------------
@app.route('/api/login', methods=['POST'])
def handle_login():
    data = request.get_json()
    user = login(data['username'], data['password'])
    if user:
        token = create_access_token(identity=user)
        return jsonify(access_token=token), 200
    return jsonify(error="Invalid credentials"), 401

# ------------------- Medicines -------------------
@app.route('/api/medicines', methods=['GET'])
def get_medicines():
    with sqlite3.connect('pharmacy.db') as db:
        medicines = db.execute('SELECT * FROM medicines').fetchall()
        return jsonify([dict(row) for row in medicines]), 200

@app.route('/api/medicines', methods=['POST'])
@role_required('admin')
def add_medicine():
    data = request.get_json()
    with sqlite3.connect('pharmacy.db') as db:
        db.execute('''
            INSERT INTO medicines (name, price, stock, expiry_date)
            VALUES (?, ?, ?, ?)
        ''', (data['name'], data['price'], data['stock'], data['expiry_date']))
    return jsonify(success=True), 201

# ------------------- Prescriptions -------------------
@app.route('/api/prescriptions', methods=['POST'])
@role_required('doctor')
def create_prescription():
    data = request.get_json()
    with sqlite3.connect('pharmacy.db') as db:
        db.execute('''
            INSERT INTO prescriptions 
            (patient_id, doctor_id, medicine_id, dosage)
            VALUES (?, ?, ?, ?)
        ''', (
            data['patient_id'],
            get_jwt_identity().get('id', None),
            data['medicine_id'],
            data['dosage']
        ))
    return jsonify(success=True), 201

if __name__ == '__main__':
    app.run(debug=False)