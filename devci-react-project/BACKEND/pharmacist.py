import sqlite3
from database import require_role

@require_role('pharmacist')
def pharmacist_dashboard(user):
    print("\n==== Pharmacist Dashboard ====\n")
    print("1. Verify Prescription")
    print("2. View Audit Log")
    print("3. Search Prescriptions by Patient Name")
    print("4. Search Prescriptions by ID")
    print("5. Logout")
    choice = input("Choose option: ")
    
    if choice == '1':
        verify_prescription(user)
    elif choice == '2':
        view_audit_log(user)
    elif choice == '3':
        search_prescriptions_by_patient_name(user)
    elif choice == '4':
        search_prescriptions_by_id(user)
    elif choice == '5':
        print("Logging out...")
    else:
        print("Invalid choice!")

def search_prescriptions_by_patient_name(pharmacist):
    print("\n--- Search Prescription by Patient Name ---")
    patient_name = input("Enter patient name: ").strip()
    
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        try:
            cursor.execute('''
                SELECT 
                    p.id,
                    pt.full_name AS patient_name,
                    p.medicine_name,
                    p.dosage,
                    p.status,
                    d.full_name AS doctor_name,
                    d.specialization,
                    p.created_at
                FROM prescriptions p
                JOIN patients pt ON p.patient_id = pt.id
                JOIN doctors d ON p.doctor_id = d.user_id
                WHERE pt.full_name = ?
            ''', (patient_name,))
            
            results = cursor.fetchall()
            
            if not results:
                print("\nNo prescriptions found for this patient.")
                return
            
            print(f"\nPrescriptions for patient '{patient_name}':")
            print("-" * 80)
            for result in results:
                print(f"Prescription ID: {result[0]}")
                print(f"Patient: {result[1]}")
                print(f"Medication: {result[2]}")
                print(f"Dosage: {result[3]}")
                print(f"Status: {result[4].upper()}")
                print(f"Prescribed by: {result[5]} ({result[6]})")
                print(f"Date: {result[7]}")
                print("-" * 80)
            
        except sqlite3.Error as e:
            print(f"Search error: {str(e)}")

def search_prescriptions_by_id(pharmacist):
    print("\n--- Search Prescription by ID ---")
    prescription_id = input("Enter prescription ID: ").strip()
    
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        try:
            cursor.execute('''
                SELECT 
                    p.id,
                    pt.full_name AS patient_name,
                    p.medicine_name,
                    p.dosage,
                    p.status,
                    d.full_name AS doctor_name,
                    d.specialization,
                    p.created_at
                FROM prescriptions p
                JOIN patients pt ON p.patient_id = pt.id
                JOIN doctors d ON p.doctor_id = d.user_id
                WHERE p.id = ?
            ''', (prescription_id,))
            
            result = cursor.fetchone()
            
            if not result:
                print("\nNo prescription found with this ID.")
                return
            
            print("\nPrescription Details:")
            print("-" * 80)
            print(f"Prescription ID: {result[0]}")
            print(f"Patient: {result[1]}")
            print(f"Medication: {result[2]}")
            print(f"Dosage: {result[3]}")
            print(f"Status: {result[4].upper()}")
            print(f"Prescribed by: {result[5]} ({result[6]})")
            print(f"Date: {result[7]}")
            print("-" * 80)
            
        except sqlite3.Error as e:
            print(f"Search error: {str(e)}")

def search_prescriptions_by_patient_email(pharmacist):
    print("\n--- Search Prescription by Patient Email ---")
    patient_email = input("Enter patient email: ").strip()
    
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        try:
            cursor.execute('''
                SELECT 
                    p.id,
                    u.email AS patient_email,
                    m.name AS medication,
                    p.dosage,
                    p.status,
                    d.full_name AS doctor_name,
                    d.specialization,
                    p.created_at
                FROM prescriptions p
                JOIN users u ON p.patient_id = u.id
                JOIN medicines m ON p.medicine_id = m.id
                JOIN doctors d ON p.doctor_id = d.user_id
                WHERE u.email = ?
            ''', (patient_email,))
            
            results = cursor.fetchall()
            
            if not results:
                print("\nNo prescriptions found for this patient.")
                return
            
            print(f"\nPrescriptions for patient with email '{patient_email}':")
            print("-" * 80)
            for result in results:
                print(f"Prescription ID: {result[0]}")
                print(f"Patient Email: {result[1]}")
                print(f"Medication: {result[2]}")
                print(f"Dosage: {result[3]}")
                print(f"Status: {result[4].upper()}")
                print(f"Prescribed by: {result[5]} ({result[6]})")
                print(f"Date: {result[7]}")
                print("-" * 80)
            
        except sqlite3.Error as e:
            print(f"Search error: {str(e)}")

def verify_prescription(pharmacist):
    print("\n--- New Prescription Verification ---")
    doctor_name = input("Doctor's name: ").strip()
    medication = input("Medication prescribed: ").strip()
    patient_name = input("Patient name: ").strip()

    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT id, specialization FROM doctors 
            WHERE full_name LIKE ? LIMIT 1
        ''', (f'%{doctor_name}%',))
        doctor = cursor.fetchone()

        if not doctor:
            print("⚠ Doctor not found in database!")
            return

        doctor_id, specialization = doctor
        
        cursor.execute('''
            SELECT id FROM patients 
            WHERE full_name LIKE ? LIMIT 1
        ''', (f'%{patient_name}%',))
        patient = cursor.fetchone()

        if not patient:
            print("⚠ Patient not found in database!")
            return

        patient_id = patient[0]
        
        cursor.execute('''
            SELECT 1 FROM medicines 
            WHERE name = ?
        ''', (medication,))
        
        is_valid = cursor.fetchone() is not None
        status = 'valid' if is_valid else 'warning'
        
        cursor.execute('''
            INSERT INTO prescriptions 
            (pharmacist_id, doctor_id, patient_id, medicine_name, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (pharmacist['id'], doctor_id, patient_id, medication, status))
        db.commit()
        
        print(f"\nVerification Result: {status.upper()}")
        if status == 'warning':
            print(f"Alert: {medication} may not be typically prescribed by {specialization}s")

def view_audit_log(pharmacist):
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        cursor.execute('''
            SELECT created_at, medicine_name, status 
            FROM prescriptions 
            WHERE pharmacist_id = ?
            ORDER BY created_at DESC LIMIT 10
        ''', (pharmacist['id'],))
        
        print("\nLast 10 Verifications:")
        for row in cursor.fetchall():
            print(f"{row[0]} | {row[1]} ({row[2].upper()})")