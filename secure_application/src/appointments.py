from database import get_connection


def book_appointment():
    """Book an appointment for an existing patient."""

    print("\n========== BOOK APPOINTMENT ==========")

    try:
        patient_id = int(input("Patient ID: "))
    except ValueError:
        print("Patient ID must be a number.")
        return

    doctor_name = input("Doctor name: ").strip()
    appointment_date = input("Appointment date (DD-MM-YYYY): ").strip()
    reason = input("Reason for appointment: ").strip()

    if not doctor_name or not appointment_date or not reason:
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

    # Insert appointment
    cursor.execute(
        """
        INSERT INTO appointments
        (patient_id, doctor_name, appointment_date, reason)
        VALUES (?, ?, ?, ?)
        """,
        (patient_id, doctor_name, appointment_date, reason)
    )

    appointment_id = cursor.lastrowid

    connection.commit()
    connection.close()

    print("\nAppointment booked successfully!")
    print(f"Appointment ID: {appointment_id}")
    print(f"Patient: {patient['name']}")


def view_appointments():
    """Display all booked appointments."""

    print("\n========== APPOINTMENTS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            a.appointment_id,
            p.patient_id,
            p.name AS patient_name,
            a.doctor_name,
            a.appointment_date,
            a.reason
        FROM appointments a
        JOIN patients p
            ON a.patient_id = p.patient_id
        ORDER BY a.appointment_id
        """
    )

    appointments = cursor.fetchall()

    connection.close()

    if not appointments:
        print("No appointments found.")
        return

    for appointment in appointments:

        print("\n------------------------------")
        print(f"Appointment ID : {appointment['appointment_id']}")
        print(f"Patient ID     : {appointment['patient_id']}")
        print(f"Patient Name   : {appointment['patient_name']}")
        print(f"Doctor         : {appointment['doctor_name']}")
        print(f"Date           : {appointment['appointment_date']}")
        print(f"Reason         : {appointment['reason']}")