import sqlite3
from database import require_role, register_user

def list_doctors():
    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT u.id, d.full_name, d.specialization, d.hospital 
            FROM doctors d 
            JOIN users u ON d.user_id = u.id
        """)
        doctors = cursor.fetchall()
        
        print("\nRegistered Doctors:")
        for doctor in doctors:
            print(f"ID: {doctor[0]} | Name: {doctor[1]} | Specialization: {doctor[2]} | Hospital: {doctor[3]}")

@require_role('admin')
def admin_dashboard(user):
    print(f"\n==== Admin Dashboard ====")
    print(user)
    while True:
        print("\n1. Register Doctor")
        print("2. List Doctors")
        print("3. Update Doctor")
        print("4. Delete Doctor")
        print("5. Return to Main Menu")
        choice = input("Choose option: ")

        if choice == '1':
            username = input("Enter doctor's username: ")
            password = input("Enter temporary password: ")
            full_name = input("Enter full name: ")
            specialization = input("Enter specialization: ")
            hospital = input("Enter hospital: ")
            
            register_user(username, password, role='doctor', full_name=full_name, specialization=specialization, hospital=hospital)
            print("✅ Doctor registered successfully!")
        elif choice == '2':
            list_doctors()
        elif choice == '3':
            update_doctor()
        elif choice == '4':
            delete_doctor()
        elif choice == '5':
            break
        else:
            print("Invalid choice!")

def update_doctor():
    user_id = input("Enter doctor's user ID to update: ").strip()
    if not user_id.isdigit():
        print("❌ Invalid ID format!")
        return

    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT full_name, specialization, hospital FROM doctors WHERE user_id = ?", (user_id,))
        doctor = cursor.fetchone()
        
        if not doctor:
            print("❌ Doctor not found!")
            return

        print(f"\nCurrent Details:")
        print(f"1. Name: {doctor[0]}")
        print(f"2. Specialization: {doctor[1]}")
        print(f"3. Hospital: {doctor[2]}")
        
        field_map = {"1": "full_name", "2": "specialization", "3": "hospital"}
        field = input("\nEnter field number to update (1-3): ")
        if field not in field_map:
            print("❌ Invalid field selection!")
            return
        
        new_value = input("Enter new value: ").strip()
        try:
            cursor.execute(f"UPDATE doctors SET {field_map[field]} = ? WHERE user_id = ?", (new_value, user_id))
            db.commit()
            print("✅ Doctor updated successfully!")
        except sqlite3.Error as e:
            print(f"❌ Update failed: {str(e)}")

def delete_doctor():
    user_id = input("Enter doctor's user ID to delete: ").strip()
    if not user_id.isdigit():
        print("❌ Invalid ID format!")
        return

    with sqlite3.connect('pharmacy.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT full_name FROM doctors WHERE user_id = ?", (user_id,))
        doctor = cursor.fetchone()
        
        if not doctor:
            print("❌ Doctor not found!")
            return

        confirm = input(f"Delete {doctor[0]} (y/n)? ").lower()
        if confirm == 'y':
            try:
                cursor.execute('DELETE FROM doctors WHERE user_id = ?', (user_id,))
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                db.commit()
                print("✅ Doctor deleted successfully!")
            except sqlite3.Error as e:
                print(f"❌ Deletion failed: {str(e)}")