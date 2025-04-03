import sqlite3
from database import require_role

@require_role('pharmacist')
def pharmacist_dashboard(user):
    print("\n==== Pharmacist Dashboard ====\n")
    print("1. Verify Prescription")
    print("2. View Audit Log")
    print("3. Search Prescriptions by Patient")
    print("4. Search Prescriptions by ID")
    print("5. Logout")
    choice = input("Choose option: ")
    
    if choice == '1':
        verify_prescription(user)
    elif choice == '2':
        view_audit_log(user)
    elif choice == '3':
        search_prescriptions_by_patient(user)
    elif choice == '4':
        search_prescriptions_by_id(user)
    elif choice == '5':
        print("Logging out...")
    else:
        print("Invalid choice!")

def search_prescriptions_by_patient(pharmacist):
    print("\n--- Search Prescriptions by Patient ---")
    patient_name = input("Enter patient name (partial or full): ").strip()
    
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        try:
            cursor.execute('''
                SELECT 
                    p.id,
                    u.username AS patient_name,
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
                WHERE u.username LIKE ?
                ORDER BY p.created_at DESC
            ''', (f'%{patient_name}%',))
            
            results = cursor.fetchall()
            
            if not results:
                print("\nNo prescriptions found for this patient.")
                return
            
            print(f"\nFound {len(results)} prescriptions for '{patient_name}':")
            print("-" * 80)
            for rx in results:
                print(f'''
                Prescription ID: {rx[0]}
                Patient: {rx[1]}
                Medication: {rx[2]}
                Dosage: {rx[3]}
                Status: {rx[4].upper()}
                Prescribed by: {rx[5]} ({rx[6]})
                Date: {rx[7]}
                ''')
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
                    u.username AS patient_name,
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

def verify_prescription(pharmacist):
    print("\n--- New Prescription Verification ---")
    doctor_name = input("Doctor's name: ").strip()
    medication = input("Medication prescribed: ").strip()
    patient_info = input("Patient info (optional): ").strip()

    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT id, specialization FROM doctors 
            WHERE full_name LIKE ? LIMIT 1
        ''', (f'%{doctor_name}%'))
        doctor = cursor.fetchone()

        if not doctor:
            print("⚠ Doctor not found in database!")
            log_prescription(pharmacist, None, medication, patient_info, 'critical')
            return

        doctor_id, specialization = doctor
        
        cursor.execute('''
            SELECT 1 FROM medicines 
            WHERE name = ?
        ''', (medication,))
        
        is_valid = cursor.fetchone() is not None
        status = 'valid' if is_valid else 'warning'
        
        log_prescription(pharmacist, doctor_id, medication, patient_info, status)
        
        print(f"\nVerification Result: {status.upper()}")
        if status == 'warning':
            print(f"Alert: {medication} may not be typically prescribed by {specialization}s")

def log_prescription(pharmacist, doctor_id, medication, patient_info, status):
    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO prescriptions 
            (pharmacist_id, doctor_id, medicine_id, patient_id, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (pharmacist['id'], doctor_id, medication, patient_info, status))
        db.commit()

def view_audit_log(pharmacist):
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        cursor.execute('''
            SELECT created_at, medicine_id, status 
            FROM prescriptions 
            WHERE pharmacist_id = ?
            ORDER BY created_at DESC LIMIT 10
        ''', (pharmacist['id'],))
        
        print("\nLast 10 Verifications:")
        for row in cursor.fetchall():
            print(f"{row[0]} | {row[1]} ({row[2].upper()})")