from flask import request, jsonify, Blueprint
import sqlite3

add_medicine_bp = Blueprint('addMedicine', __name__)

@add_medicine_bp.route('/addmedicine', methods=["POST"])
def add_medicine():
    data = request.get_json() 
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    medicine_name = data.get('medicine_name')
    price = data.get('price')
    stock = data.get('stock')
    expiry_date = data.get('expiry_date')
    
    if not all([medicine_name, price, stock, expiry_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    with sqlite3.connect('pharmacy.db') as conn:  
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO medicines(name, price, stock, expiry_date) 
                VALUES (?, ?, ?, ?)
            ''', (medicine_name, price, stock, expiry_date))
            conn.commit()
            return jsonify({'message': "Medicine added successfully"}), 201
        except sqlite3.Error as e:
            print(e)
            return jsonify({'error': str(e)}), 500