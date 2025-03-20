# doctor.py
import sqlite3
from database import require_role

@require_role('doctor')
def doctor_dashboard(user):
    print(f"\n==== Doctor Dashboard ====")
    while True:
        print("\n1. Write New Prescription")
        print("2. View My Prescriptions")
        print("3. Logout")
        choice = input("Choose option: ")

        if choice == '1':
            write_prescription(user)
        elif choice == '2':
            view_prescriptions(user)
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

def write_prescription(doctor):
    print("\n--- New Prescription ---")
    patient_name = input("Patient's Full Name: ")
    patient_age = input("Patient's Age: ")
    patient_contact = input("Contact Info: ")
    medication = input("Medication: ")
    dosage = input("Dosage: ")
    instructions = input("Instructions: ")

    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO prescriptions 
            (doctor_id, patient_name, patient_age, patient_contact, 
             medication, dosage, instructions, verification_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
        ''', (doctor['id'], patient_name, patient_age, patient_contact, 
              medication, dosage, instructions))
        db.commit()
    print("✅ Prescription created successfully!")

def view_prescriptions(doctor):
    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.execute('''
            SELECT prescription_id, patient_name, medication, timestamp 
            FROM prescriptions 
            WHERE doctor_id = ?
            ORDER BY timestamp DESC
        ''', (doctor['id'],))
        
        print("\nYour Recent Prescriptions:")
        for rx in cursor.fetchall():
            print(f"{rx[3]} | {rx[1]} | {rx[2]} (ID: {rx[0]})")