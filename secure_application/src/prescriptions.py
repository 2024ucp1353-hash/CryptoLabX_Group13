from database import get_connection


def add_prescription():
    """Add a prescription for an existing patient."""

    print("\n========== ADD PRESCRIPTION ==========")

    try:
        patient_id = int(input("Patient ID: "))
    except ValueError:
        print("Patient ID must be a number.")
        return

    doctor_name = input("Doctor name: ").strip()
    medicine = input("Medicine: ").strip()
    dosage = input("Dosage: ").strip()

    if not doctor_name or not medicine or not dosage:
        print("All fields are required.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    # Check whether patient exists
    cursor.execute(
        "SELECT patient_id, name FROM patients WHERE patient_id = ?",
        (patient_id,)
    )

    patient = cursor.fetchone()

    if not patient:
        connection.close()
        print("Patient not found.")
        return

    # Add prescription
    cursor.execute(
        """
        INSERT INTO prescriptions
        (patient_id, doctor_name, medicine, dosage)
        VALUES (?, ?, ?, ?)
        """,
        (patient_id, doctor_name, medicine, dosage)
    )

    prescription_id = cursor.lastrowid

    connection.commit()
    connection.close()

    print("\nPrescription added successfully!")
    print(f"Prescription ID: {prescription_id}")
    print(f"Patient: {patient['name']}")


def view_prescriptions():
    """Display all prescriptions."""

    print("\n========== PRESCRIPTIONS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            pr.prescription_id,
            p.patient_id,
            p.name AS patient_name,
            pr.doctor_name,
            pr.medicine,
            pr.dosage
        FROM prescriptions pr
        JOIN patients p
            ON pr.patient_id = p.patient_id
        ORDER BY pr.prescription_id
        """
    )

    prescriptions = cursor.fetchall()

    connection.close()

    if not prescriptions:
        print("No prescriptions found.")
        return

    for prescription in prescriptions:

        print("\n------------------------------")
        print(f"Prescription ID : {prescription['prescription_id']}")
        print(f"Patient ID      : {prescription['patient_id']}")
        print(f"Patient Name    : {prescription['patient_name']}")
        print(f"Doctor          : {prescription['doctor_name']}")
        print(f"Medicine        : {prescription['medicine']}")
        print(f"Dosage          : {prescription['dosage']}")