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
    print("Database initialized successfully!")
    with sqlite3.connect('pharmacy.db') as conn:
        # conn = sqlite3('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute('''
            PRAGMA foreign_keys = ON;

            -- Core Tables
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
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

            -- Prescriptions
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL REFERENCES users(id),
                doctor_name TEXT NOT NULL,
                pharmacist_id INTEGER,
                patient_name TEXT NOT NULL,
                patient_age TEXT NOT NULL,
                contact TEXT,
                medicine_id INTEGER NOT NULL REFERENCES medicines(id),
                medicine_name TEXT NOT NULL,
                dosage TEXT NOT NULL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'filled', 'rejected')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            );
        ''')
        conn.commit()

def register_user(username, password, role, **kwargs):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        # 1. Insert into users table
        cursor.execute('''
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        ''', (username, hashed_pw, role))
        
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

def login(username, password):
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, password_hash, role FROM users WHERE username = ?
        ''', (username,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode(), user[1].encode()):
            return {'id': user[0], 'role': user[2]}
        return None