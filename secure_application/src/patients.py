from database import get_connection


def register_patient():
    """Register a new patient in the hospital database."""

    print("\n========== PATIENT REGISTRATION ==========")

    name = input("Patient name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    try:
        age = int(input("Age: "))

        if age <= 0 or age > 120:
            print("Please enter a valid age.")
            return

    except ValueError:
        print("Age must be a number.")
        return

    gender = input("Gender: ").strip()
    phone = input("Phone: ").strip()
    address = input("Address: ").strip()

    if not gender or not phone or not address:
        print("Gender, phone and address cannot be empty.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO patients
        (name, age, gender, phone, address)
        VALUES (?, ?, ?, ?, ?)
    """

    cursor.execute(
        query,
        (name, age, gender, phone, address)
    )

    patient_id = cursor.lastrowid

    connection.commit()
    connection.close()

    print("\nPatient registered successfully!")
    print(f"Patient ID: {patient_id}")


def view_all_patients():
    """Display all registered patients."""

    print("\n========== ALL PATIENTS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT patient_id, name, age, gender, phone, address
        FROM patients
        ORDER BY patient_id
    """)

    patients = cursor.fetchall()

    connection.close()

    if not patients:
        print("No patients registered.")
        return

    for patient in patients:
        print("\n------------------------------")
        print(f"Patient ID : {patient['patient_id']}")
        print(f"Name       : {patient['name']}")
        print(f"Age        : {patient['age']}")
        print(f"Gender     : {patient['gender']}")
        print(f"Phone      : {patient['phone']}")
        print(f"Address    : {patient['address']}")