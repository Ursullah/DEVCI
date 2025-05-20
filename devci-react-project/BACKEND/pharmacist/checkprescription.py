# Temporary debug route
from flask import jsonify, Blueprint
import sqlite3

debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/debug', methods=['GET'])
def debug_prescriptions():
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prescriptions")
        columns = [desc[0] for desc in cursor.description]
        pharmacists = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(pharmacists)