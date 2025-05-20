import sqlite3

def recreate_prescriptions_table():
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        # Disable foreign key constraints temporarily
        cursor.execute("PRAGMA foreign_keys=OFF")
        
        # Drop the existing table if it exists
        cursor.execute("DROP TABLE IF EXISTS prescriptions")
        
        # Recreate the table with the new schema
        cursor.execute('''
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
                instructions TEXT,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'filled', 'rejected')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            );
        ''')
        
        # Re-enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys=ON")
        
        print("Prescriptions table recreated successfully!")
        conn.commit()

if __name__ == "__main__":
    recreate_prescriptions_table()