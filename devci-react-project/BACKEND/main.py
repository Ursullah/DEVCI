from database import init_db, register_user, login, add_patient
from pharmacist import pharmacist_dashboard
from admin import admin_dashboard
from doctor import doctor_dashboard

def main_menu():
    print("\n==== Pharmacy System ====")
    print("1. Register New User")
    print("2. Login")
    print("3. Add Patient (Record Keeping)")  # New option for adding patients
    print("4. Exit")
    return input("Choose option: ")

if __name__ == "_main_":
    init_db()
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            print("\n--- User Registration ---")
            role = input("Role (doctor/pharmacist/admin): ").lower()
            
            if role not in ['doctor', 'pharmacist', 'admin']:
                print("Invalid role!")
                continue
                
            email = input("Email: ")
            password = input("Password: ")
            full_name = input("Full Name: ")

            try:
                if role == 'doctor':
                    specialization = input("Specialization: ")
                    hospital = input("Hospital: ")
                    register_user(email, password, role, full_name=full_name, specialization=specialization, hospital=hospital)
                elif role == 'pharmacist':
                    license_number = input("License Number: ")
                    register_user(email, password, role, full_name=full_name, license_number=license_number)
                elif role == 'admin':
                    access_level = input("Access Level (basic/super): ")
                    register_user(email, password, role, full_name=full_name, access_level=access_level)
                        
                print("✅ Registration successful!")
                
            except Exception as e:
                print(f"❌ Registration failed: {str(e)}")
                
        elif choice == '2':
            print("\n--- Login ---")
            email = input("Email: ")
            password = input("Password: ")
            user = login(email, password)
            
            if user:
                if user['role'] == 'pharmacist':
                    pharmacist_dashboard(user)
                elif user['role'] == 'admin':
                    admin_dashboard(user)
                elif user['role'] == 'doctor':
                    doctor_dashboard(user)
            else:
                print("❌ Invalid credentials!")
        
        elif choice == '3':  # New option for adding patients
            print("\n--- Add Patient (Record Keeping) ---")
            full_name = input("Full Name: ")
            date_of_birth = input("Date of Birth (YYYY-MM-DD): ")
            contact_number = input("Contact Number: ")
            address = input("Address: ")
            medical_history = input("Medical History: ")

            try:
                add_patient(full_name, date_of_birth, contact_number, address, medical_history)
                print("✅ Patient added successfully!")
            except Exception as e:
                print(f"❌ Failed to add patient: {str(e)}")
        
        elif choice == '4':
            print("Exiting........")
            break
            
        else:
            print("Invalid choice!")