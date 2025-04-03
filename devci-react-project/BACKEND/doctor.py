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
    patient_name = input("Patient full name: ")
    medicine_name = input("Medication name: ")
    dosage = input("Dosage: ")

    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        # Verify if the patient exists in the patients table
        cursor.execute('SELECT id FROM patients WHERE full_name = ?', (patient_name,))
        patient = cursor.fetchone()
        
        if not patient:
            print("❌ Error: No patient found with this name.")
            return
        
        patient_id = patient[0]
        
        # Insert the prescription
        cursor.execute('''
            INSERT INTO prescriptions 
            (doctor_id, patient_id, medicine_name, dosage, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (doctor['id'], patient_id, medicine_name, dosage))
        db.commit()
    print("✅ Prescription created successfully!")

def view_prescriptions(doctor):
    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        cursor.execute('''
            SELECT 
                p.id, 
                pt.full_name AS patient_name, 
                p.medicine_name, 
                p.dosage, 
                p.status, 
                p.created_at 
            FROM prescriptions p
            JOIN patients pt ON p.patient_id = pt.id
            WHERE p.doctor_id = ?
            ORDER BY p.created_at DESC
        ''', (doctor['id'],))
        
        print("\nYour Recent Prescriptions:")
        for rx in cursor.fetchall():
            print(f"{rx[5]} | Patient name: {rx[1]} | Medicine: {rx[2]} | Dosage: {rx[3]} | Status: {rx[4]} (ID: {rx[0]})")