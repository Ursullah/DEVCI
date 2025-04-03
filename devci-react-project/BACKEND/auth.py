import sqlite3
import random
from datetime import datetime, timedelta

def generate_random_date():
    start_date = datetime.now()
    end_date = start_date + timedelta(days=random.randint(30, 365 * 5))  # Expiry within 5 years
    return end_date.strftime('%Y-%m-%d')

def populate_medicines():
    medicines = [
        # Cardiology
        "Aspirin", "Metoprolol", "Atorvastatin", "Enalapril", "Losartan", "Clopidogrel", "Warfarin", "Simvastatin",
        "Diltiazem", "Propranolol",
        # Neurology
        "Gabapentin", "Levetiracetam", "Carbamazepine", "Phenytoin", "Topiramate", "Ropinirole", "Rivastigmine",
        "Sumatriptan", "Zolmitriptan", "Dopamine",
        # Dermatology
        "Hydrocortisone Cream", "Benzoyl Peroxide", "Tretinoin", "Ketoconazole", "Mupirocin", "Clotrimazole",
        "Adapalene", "Tacrolimus", "Salicylic Acid", "Isotretinoin",
        # Pediatrics
        "Paracetamol Syrup", "Amoxicillin Suspension", "Cefixime", "Ibuprofen Syrup", "Montelukast", "Diphenhydramine",
        "Vitamin D Drops", "Zinc Syrup", "Lactulose", "Domperidone",
        # Ophthalmology
        "Latanoprost", "Timolol Eye Drops", "Ciprofloxacin Eye Drops", "Olopatadine", "Bimatoprost", "Brimonidine",
        "Fluorometholone", "Pilocarpine", "Tobramycin", "Dorzolamide",
        # General Physician
        "Omeprazole", "Ranitidine", "Metformin", "Ciprofloxacin", "Azithromycin", "Loratadine", "Doxycycline",
        "Ibuprofen", "Acetaminophen", "Cough Syrup",
    ]
    
    with sqlite3.connect('pharmacy.db') as conn:
        cursor = conn.cursor()
        
        for medicine in medicines:
            price = round(random.uniform(5, 200), 2)  # Random price between $5 and $200
            stock = random.randint(10, 500)  # Random stock between 10 and 500
            expiry_date = generate_random_date()
            
            cursor.execute('''
                INSERT INTO medicines (name, price, stock, expiry_date)
                VALUES (?, ?, ?, ?)
            ''', (medicine, price, stock, expiry_date))
        
        conn.commit()
        print("Medicines inserted successfully!")

if __name__ == "__main__":
    populate_medicines()