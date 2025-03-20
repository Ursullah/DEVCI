import sqlite3
from database import require_role;
from database import register_doctor, list_doctors
import hashlib

@require_role('admin')
def admin_dashboard(user):
    print(f"\n==== Admin Dashboard ====")
    while True:
        print("\n1. Register Doctor")
        print("2. List Doctors")
        print("3. Update Doctor")
        print("4. Delete Doctor")
        print("5. Return to Main Menu")
        choice = input("Choose option: ")

        if choice == '1':
            # Collect doctor details
            username = input("Enter doctor's username: ")
            password = input("Enter temporary password: ")
            full_name = input("Enter full name: ")
            specialization = input("Enter specialization: ")
            hospital = input("Enter hospital: ")
            
            register_doctor(username, password, full_name, specialization, hospital)

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
        print("â Invalid ID format!")
        return

    with sqlite3.connect('pharmacy.db') as db:
        doctor = db.execute('''
            SELECT * FROM doctors WHERE user_id = ?
        ''', (user_id,)).fetchone()
        
        if not doctor:
            print("â Doctor not found!")
            return

        print(f"\nCurrent Details:")
        print(f"1. Name: {doctor[1]}")
        print(f"2. Specialization: {doctor[2]}")
        print(f"3. Hospital: {doctor[3]}")
        
        field = input("\nEnter field number to update (1-3): ")
        new_value = input("Enter new value: ").strip()
        
        fields = ['name', 'specialization', 'hospital']
        if not field.isdigit() or int(field) not in range(1,4):
            print("â Invalid field selection!")
            return

        try:
            db.execute(f'''
                UPDATE doctors 
                SET {fields[int(field)-1]} = ? 
                WHERE user_id = ?
            ''', (new_value, user_id))
            db.commit()
            print("â Doctor updated successfully!")
        except sqlite3.Error as e:
            print(f"â Update failed: {str(e)}")

def delete_doctor():
    user_id = input("Enter doctor's user ID to delete: ").strip()
    if not user_id.isdigit():
        print("â Invalid ID format!")
        return

    with sqlite3.connect('pharmacy.db') as db:
        doctor = db.execute('''
            SELECT * FROM doctors WHERE user_id = ?
        ''', (user_id,)).fetchone()
        
        if not doctor:
            print("â Doctor not found!")
            return

        confirm = input(f"Delete {doctor[1]} (y/n)? ").lower()
        if confirm == 'y':
            try:
                # Delete from both doctors and users tables
                db.execute('DELETE FROM doctors WHERE user_id = ?', (user_id,))
                db.execute('DELETE FROM users WHERE id = ?', (user_id,))
                db.commit()
                print("â Doctor deleted successfully!")
            except sqlite3.Error as e:
                print(f"â Deletion failed: {str(e)}")