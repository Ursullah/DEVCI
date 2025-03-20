import sqlite3
import hashlib
from contextlib import closing

# Database initialization
def init_db():
    with sqlite3.connect('pharmacy.db', timeout=10) as db:  # Timeout added
        cursor = db.cursor()
        cursor.executescript('''
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('pharmacist', 'admin', 'doctor'))
            );
                             
             CREATE TABLE IF NOT EXISTS pharmacists (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                license_number TEXT UNIQUE,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                access_level TEXT CHECK(access_level IN ('basic', 'super')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );                

            CREATE TABLE IF NOT EXISTS doctors (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                hospital TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS specializations (
                specialization TEXT NOT NULL,
                allowed_medication TEXT NOT NULL,
                PRIMARY KEY (specialization, allowed_medication)
            );

            CREATE TABLE IF NOT EXISTS prescriptions (
                prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                patient_name TEXT NOT NULL,
                patient_age INTEGER,
                patient_contact TEXT,
                medication TEXT NOT NULL,
                dosage TEXT NOT NULL,
                instructions TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                verification_status TEXT CHECK(verification_status IN ('pending', 'valid', 'warning', 'critical')),
                pharmacist_id INTEGER,
                FOREIGN KEY (doctor_id) REFERENCES doctors(user_id) ON DELETE CASCADE,
                FOREIGN KEY (pharmacist_id) REFERENCES users(id)
            );
        ''')
        db.commit()

if __name__ == "__main__":
    init_db()
    print("Database created: pharmacy.db")

# User registration/login
def register_user(username, password, role, full_name, license_or_access):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            ''', (username, password_hash, role))
            
            user_id = cursor.lastrowid
            
            if role == 'pharmacist':
                cursor.execute('''
                    INSERT INTO pharmacists (user_id, full_name, license_number)
                    VALUES (?, ?, ?)
                ''', (user_id, full_name, license_or_access))
            elif role == 'admin':
                cursor.execute('''
                    INSERT INTO admins (user_id, full_name, access_level)
                    VALUES (?, ?, ?)
                ''', (user_id, full_name, license_or_access))
            elif role == 'doctor':
                cursor.execute('''
                    INSERT INTO doctors (user_id, name, specialization, hospital)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, full_name, license_or_access, "Unknown Hospital"))
            
            db.commit()
            print(f"User {username} registered successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error: {str(e)}")



def register_doctor(username, password, full_name, specialization, hospital):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        try:
            # Create user account
            cursor.execute('''
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, 'doctor')
            ''', (username, password_hash))
            
            user_id = cursor.lastrowid
            
            # Create doctor profile
            cursor.execute('''
                INSERT INTO doctors (user_id, name, specialization, hospital)
                VALUES (?, ?, ?, ?)
            ''', (user_id, full_name, specialization, hospital))
            
            db.commit()
            print(f"Doctor {username} registered successfully!")
            
        except sqlite3.IntegrityError as e:
            print(f"Error: {str(e)}")


# Add this function to your database.py file
def list_doctors():
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        cursor.execute('''
            SELECT d.user_id, d.name, d.specialization, d.hospital, u.username 
            FROM doctors d
            JOIN users u ON d.user_id = u.id
        ''')
        doctors = cursor.fetchall()
        print("\n--- Registered Doctors ---")
        for doc in doctors:
            print(f"ID: {doc[0]} | {doc[1]} ({doc[2]} at {doc[3]}) | Username: {doc[4]}")

def login(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        cursor.execute('''
            SELECT id, role FROM users
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        user = cursor.fetchone()
        return {'id': user[0], 'role': user[1]} if user else None

def require_role(role):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user['role'] != role:
                print(f"Access denied! Requires {role} privileges.")
                return
            return func(user, *args, **kwargs)
        return wrapper
    return decorator
