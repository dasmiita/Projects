import mysql.connector
# Database connection setup


db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="maybe21",
    database="hospitals"
)
cursor = db_connection.cursor()

# Function to select doctor's specialty
def select_speciality():
    specialties = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'General Surgery', 'Dermatology', 'Psychiatry']
    print("Select Specialty:")
    for idx, speciality in enumerate(specialties, 1):
        print(f"{idx}. {speciality}")
    
    choice = int(input("Enter the number corresponding to the specialty: ").strip())
    
    if 1 <= choice <= len(specialties):
        return specialties[choice - 1]
    else:
        print("Invalid selection, please try again.")
        return select_speciality()

# --- Patient Management Section ---
def add_patient():
    name = input("Enter patient name: ").strip()
    age = int(input("Enter patient age: ").strip())
    address = input("Enter patient address: ").strip()
    appointment = input("Enter appointment date and time (YYYY-MM-DD HH:MM): ").strip()
    
    try:
        cursor.execute("INSERT INTO patients (name, age, address, appointment) VALUES (%s, %s, %s, %s)", 
                       (name, age, address, appointment))
        db_connection.commit()
        print(f"Patient '{name}' added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def display_patients():
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    
    if not patients:
        print("No patients found.")
    else:
        for patient in patients:
            print(f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Address: {patient[3]}, Appointment: {patient[4]}")

def update_appointment():
    name = input("Enter patient name to update appointment: ").strip()
    new_appointment = input("Enter new appointment date and time (YYYY-MM-DD HH:MM): ").strip()
    
    cursor.execute("UPDATE patients SET appointment = %s WHERE name = %s", (new_appointment, name))
    db_connection.commit()
    
    if cursor.rowcount > 0:
        print("Appointment updated.")
    else:
        print("Patient not found.")

def admit_patient():
    pid = input("Enter Patient ID: ").strip()
    room = input("Enter Room Number: ").strip()
    diagnosis = input("Enter Diagnosis: ").strip()
    
    cursor.execute("INSERT INTO patients_in_hospital (patient_id, room_number, diagnosis) VALUES (%s, %s, %s)", (pid, room, diagnosis))
    db_connection.commit()
    print(f"Patient {pid} admitted successfully!")

def discharge_patient():
    pid = input("Enter Patient ID to discharge: ").strip()
    
    cursor.execute("DELETE FROM patients_in_hospital WHERE patient_id = %s", (pid,))
    db_connection.commit()
    
    if cursor.rowcount > 0:
        print(f"Patient {pid} discharged successfully.")
    else:
        print("Patient not found.")

def list_inpatients():
    cursor.execute("SELECT * FROM patients_in_hospital")
    inpatients = cursor.fetchall()
    
    if not inpatients:
        print("No patients in the hospital.")
    else:
        for inpatient in inpatients:
            print(f"Patient ID: {inpatient[0]}, Room: {inpatient[1]}, Diagnosis: {inpatient[2]}")

# --- Doctor Management Section ---
def add_doctor():
    name = input("Enter doctor name: ").strip()
    speciality = select_speciality()
    experience = int(input("Enter doctor experience: ").strip())
    
    cursor.execute("INSERT INTO doctors (name, speciality, experience) VALUES (%s, %s, %s)", (name, speciality, experience))
    db_connection.commit()
    print(f"Doctor '{name}' added successfully!")

def display_doctors():
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    
    if not doctors:
        print("No doctors found.")
    else:
        for doctor in doctors:
            print(f"ID: {doctor[0]}, Name: {doctor[1]}, Speciality: {doctor[2]}, Experience: {doctor[3]}")

# --- Appointment Management Section ---
from datetime import datetime

def create_appointment():
    patient_id = input("Enter patient ID: ").strip()  # Assuming you're entering patient ID, not name
    doctor_id = input("Enter doctor ID: ").strip()  # Assuming you're entering doctor ID, not name
    date = input("Enter appointment date (YYYY-MM-DD): ").strip()
    time = input("Enter appointment time (HH:MM): ").strip()

    # Combine date and time into a single datetime object
    try:
        appointment_date = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date or time format.")
        return

    cursor.execute(
        "INSERT INTO appointments (patient_id, doctor_id, appointment_date) VALUES (%s, %s, %s)",
        (patient_id, doctor_id, appointment_date)
    )
    db_connection.commit()
    print("Appointment created successfully.")


    print(f"Appointment for '{patient_id}' created successfully!")

def display_appointments():
    cursor.execute("SELECT id, patient_id, doctor_id, appointment_date FROM appointments")
    appointments = cursor.fetchall()

    for appointment in appointments:
        # Assuming appointment[3] is a datetime object, we can split date and time here
        appointment_date = appointment[3]
        date_str = appointment_date.strftime("%Y-%m-%d")  # Extract date
        time_str = appointment_date.strftime("%H:%M:%S")  # Extract time

        print(f"ID: {appointment[0]}, Patient ID: {appointment[1]}, Doctor ID: {appointment[2]}, Date: {date_str}, Time: {time_str}")

# --- Billing Management Section ---
def generate_bill():
    patient_id = input("Enter Patient ID: ").strip()
    amount = float(input("Enter Bill Amount: ").strip())
    
    cursor.execute("INSERT INTO bills (patient_id, amount) VALUES (%s, %s)", (patient_id, amount))
    db_connection.commit()
    print("Bill generated successfully!")

def view_bills():
    cursor.execute("SELECT * FROM bills")
    bills = cursor.fetchall()
    
    if not bills:
        print("No bills available.")
    else:
        for bill in bills:
            print(f"ID: {bill[0]}, Patient ID: {bill[1]}, Amount: {bill[2]}")

# --- Pharmacy Management Section ---
def add_medicine():
    name = input("Enter Medicine Name: ").strip()
    quantity = int(input("Enter Quantity: ").strip())
    price = float(input("Enter Price: ").strip())
    
    cursor.execute("INSERT INTO pharmacy (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
    db_connection.commit()
    print(f"Medicine '{name}' added successfully!")

def view_pharmacy_stock():
    cursor.execute("SELECT * FROM pharmacy")
    medicines = cursor.fetchall()
    
    if not medicines:
        print("No medicines in stock.")
    else:
        for medicine in medicines:
            print(f"ID: {medicine[0]}, Name: {medicine[1]}, Quantity: {medicine[2]}, Price: {medicine[3]}")

# Close the database connection when done
def close_connection():
    if cursor:
        cursor.close()
    if db_connection:
        db_connection.close()
