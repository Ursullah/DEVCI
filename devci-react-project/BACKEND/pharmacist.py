import sqlite3
from database import require_role

@require_role('pharmacist')
def pharmacist_dashboard(user):
    print(f"\n==== Pharmacist Dashboard ====")
    while True:
        print("\n1. Verify Prescription")
        print("2. View Audit Log")
        print("3. Logout")
        choice = input("Choose option: ")

        if choice == '1':
            verify_prescription(user)
        elif choice == '2':
            view_audit_log(user)
        elif choice == '3':
            break
        else:
            print("Invalid choice!")
    # ... (pharmacist menu and verification logic)

def verify_prescription(pharmacist):
    print("\n--- New Prescription Verification ---")
    doctor_name = input("Doctor's name: ").strip()
    medication = input("Medication prescribed: ").strip()
    patient_info = input("Patient info (optional): ").strip()

    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        
        # Find doctor
        cursor.execute('''
            SELECT id, specialization FROM doctors 
            WHERE name LIKE ? LIMIT 1
        ''', (f'%{doctor_name}%',))
        doctor = cursor.fetchone()

        if not doctor:
            print("⚠️ Doctor not found in database!")
            log_prescription(pharmacist, None, medication, patient_info, 'critical')
            return

        doctor.user_id, specialization = doctor
        
        # Check medication against specialization
        cursor.execute('''
            SELECT 1 FROM specializations 
            WHERE specialization = ? AND allowed_medication = ?
        ''', (specialization, medication.lower()))
        
        is_valid = cursor.fetchone() is not None
        status = 'valid' if is_valid else 'warning'
        
        # Log prescription
        log_prescription(pharmacist, doctor.user_id, medication, patient_info, status)
        
        print(f"\nVerification Result: {status.upper()}")
        if status == 'warning':
            print(f"Alert: {medication} not typically prescribed by {specialization}s")
    # ... (prescription verification code)

def log_prescription(pharmacist, doctor_id, medication, patient_info, status):
    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO prescriptions 
            (pharmacist_id, doctor_id, medication, patient_info, verification_status)
            VALUES (?, ?, ?, ?, ?)
        ''', (pharmacist['id'], doctor_id, medication, patient_info, status))
        db.commit()

def view_audit_log(pharmacist):
    with sqlite3.connect('pharmacy.db', timeout=10) as db:
        cursor = db.cursor()
        cursor.execute('''
            SELECT timestamp, medication, verification_status 
            FROM prescriptions 
            WHERE pharmacist_id = ?
            ORDER BY timestamp DESC LIMIT 10
        ''', (pharmacist['id'],))
        
        print("\nLast 10 Verifications:")
        for row in cursor.fetchall():
            print(f"{row[0]} | {row[1]} ({row[2].upper()})")

            def search_prescriptions(pharmacist):
                patient_name = input("Enter patient name: ").strip()
                with sqlite3.connect('pharmacy.db', timeout=10) as db:
                    cursor = db.execute('''
                        SELECT p.*, d.name AS doctor_name 
                        FROM prescriptions p
                        JOIN doctors d ON p.doctor_id = d.user_id
                        WHERE patient_name LIKE ? 
                        ORDER BY timestamp DESC
                    ''', (f'%{patient_name}%',))
        
        print("\n--- Prescription Search Results ---")
        for rx in cursor.fetchall():
            print(f"""
            Prescription ID: {rx[0]}
            Patient: {rx[2]} (Age: {rx[3]}, Contact: {rx[4]})
            Medication: {rx[5]} | Dosage: {rx[6]}
            Instructions: {rx[7]}
            Prescribed by: {rx[10]} on {rx[8]}
            Status: {rx[9].upper()}
            """)