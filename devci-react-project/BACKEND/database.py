import sqlite3
import bcrypt
from functools import wraps
from contextlib import closing

# Role-based access control decorator
def require_role(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get('role') != required_role:
                print(f"Access Denied! This action requires {required_role} privileges.")
                return None
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

def init_db():
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        # Check if the prescriptions table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prescriptions';")
        table_exists = cursor.fetchone()

        if table_exists:
            print("Dropping existing prescriptions table...")
            cursor.execute("DROP TABLE prescriptions;")

        cursor.executescript('''
            PRAGMA foreign_keys = ON;

            -- Core Tables
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('pharmacist', 'admin', 'doctor', 'patient'))
            );

            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                expiry_date DATE NOT NULL
            );

            -- Role-Specific Tables
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
                full_name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                hospital TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            -- Patient Table
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                date_of_birth DATE,
                contact_number TEXT,
                address TEXT,
                medical_history TEXT
            );

            -- Create the updated prescriptions table
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                patient_id INTEGER NOT NULL,
                medicine_name TEXT NOT NULL,
                dosage TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (doctor_id) REFERENCES users (id),
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            );
        ''')
        conn.commit()

def register_user(email, password, role, **kwargs):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        # 1. Insert into users table
        cursor.execute('''
            INSERT INTO users (email, password_hash, role)
            VALUES (?, ?, ?)
        ''', (email, hashed_pw, role))
        
        user_id = cursor.lastrowid
        
        # 2. Insert into role-specific table
        if role == 'pharmacist':
            cursor.execute('''
                INSERT INTO pharmacists (user_id, full_name, license_number)
                VALUES (?, ?, ?)
            ''', (user_id, kwargs['full_name'], kwargs['license_number']))
        
        elif role == 'admin':
            cursor.execute('''
                INSERT INTO admins (user_id, full_name, access_level)
                VALUES (?, ?, ?)
            ''', (user_id, kwargs['full_name'], kwargs['access_level']))
        
        elif role == 'doctor':
            cursor.execute('''
                INSERT INTO doctors (user_id, full_name, specialization, hospital)
                VALUES (?, ?, ?, ?)
            ''', (user_id, kwargs['full_name'], kwargs['specialization'], kwargs['hospital']))
        
        conn.commit()

def login(email, password):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, password_hash, role FROM users WHERE email = ?
        ''', (email,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode(), user[1].encode()):
            return {'id': user[0], 'role': user[2]}
        return None

def add_patient(full_name, date_of_birth, contact_number, address, medical_history):
    # Code to insert a new patient record into the database
    pass

def get_patient_by_name(full_name):
    # Code to retrieve a patient record by name
    pass