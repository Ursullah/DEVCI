from flask import jsonify, Blueprint, request
import sqlite3

medicine_bp = Blueprint('medicine', __name__)

@medicine_bp.route('/medicines', methods=['GET'])
def get_medicines():
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, price, stock, expiry_date FROM medicines")
            
            medicines = []
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                medicines.append(dict(zip(columns, row)))
                
            return jsonify({'medicines': medicines})
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
        
@medicine_bp.route('/searchmedicine', methods=["GET"])
def search_medicine():
    search_term = request.args.get('name', '').strip()
    
    if not search_term:
        return jsonify({'error': 'Medicine name parameter is required'}), 400
    
    with sqlite3.connect('pharmacy.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, name, price, stock, expiry_date
                FROM medicines
                WHERE LOWER(name) LIKE LOWER(?)
                ORDER BY name           
                ''', (f'%{search_term}%',))
            
            medicines = [dict(row) for row in cursor.fetchall()]
            
            if not medicines:
                return jsonify({'message': 'No medicine found'}), 404
            
            return jsonify(medicines), 200
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
    
