from database import get_connection


def add_medical_record():
    """Add a medical record for an existing patient."""

    print("\n========== ADD MEDICAL RECORD ==========")

    try:
        patient_id = int(input("Patient ID: "))
    except ValueError:
        print("Patient ID must be a number.")
        return

    diagnosis = input("Diagnosis: ").strip()
    treatment = input("Treatment: ").strip()
    record_file = input("Record file name (optional): ").strip()

    if not diagnosis or not treatment:
        print("Diagnosis and treatment are required.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT patient_id, name FROM patients WHERE patient_id = ?",
        (patient_id,)
    )

    patient = cursor.fetchone()

    if not patient:
        connection.close()
        print("Patient not found.")
        return

    cursor.execute(
        """
        INSERT INTO medical_records
        (patient_id, diagnosis, treatment, record_file)
        VALUES (?, ?, ?, ?)
        """,
        (patient_id, diagnosis, treatment, record_file)
    )

    record_id = cursor.lastrowid

    connection.commit()
    connection.close()

    print("\nMedical record added successfully!")
    print(f"Record ID: {record_id}")
    print(f"Patient: {patient['name']}")


def view_medical_records():
    """Display all medical records."""

    print("\n========== MEDICAL RECORDS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            mr.record_id,
            p.patient_id,
            p.name AS patient_name,
            mr.diagnosis,
            mr.treatment,
            mr.record_file
        FROM medical_records mr
        JOIN patients p
            ON mr.patient_id = p.patient_id
        ORDER BY mr.record_id
        """
    )

    records = cursor.fetchall()

    connection.close()

    if not records:
        print("No medical records found.")
        return

    for record in records:
        print("\n------------------------------")
        print(f"Record ID    : {record['record_id']}")
        print(f"Patient ID   : {record['patient_id']}")
        print(f"Patient Name : {record['patient_name']}")
        print(f"Diagnosis    : {record['diagnosis']}")
        print(f"Treatment    : {record['treatment']}")
        print(f"Record File  : {record['record_file'] or 'None'}")