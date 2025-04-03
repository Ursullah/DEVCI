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
    patient_id = input("Patient ID: ")
    medicine_id = input("Medicine ID: ")
    dosage = input("Dosage: ")

    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO prescriptions 
            (doctor_id, patient_id, medicine_id, dosage, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (doctor['id'], patient_id, medicine_id, dosage))
        db.commit()
    print("✅ Prescription created successfully!")

def view_prescriptions(doctor):
    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        cursor.execute('''
            SELECT id, patient_id, medicine_id, dosage, status, created_at 
            FROM prescriptions 
            WHERE doctor_id = ?
            ORDER BY created_at DESC
        ''', (doctor['id'],))
        
        print("\nYour Recent Prescriptions:")
        for rx in cursor.fetchall():
            print(f"{rx[5]} | Patient ID: {rx[1]} | Medicine ID: {rx[2]} | Dosage: {rx[3]} | Status: {rx[4]} (ID: {rx[0]})")