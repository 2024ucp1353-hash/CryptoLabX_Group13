from database import get_connection


def create_bill():
    """Create a bill for an existing patient."""

    print("\n========== CREATE BILL ==========")

    try:
        patient_id = int(input("Patient ID: "))
    except ValueError:
        print("Patient ID must be a number.")
        return

    try:
        amount = float(input("Bill amount: "))

        if amount <= 0:
            print("Bill amount must be greater than zero.")
            return

    except ValueError:
        print("Bill amount must be a number.")
        return

    description = input("Description: ").strip()

    if not description:
        print("Description cannot be empty.")
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

    # Create bill
    cursor.execute(
        """
        INSERT INTO bills
        (patient_id, amount, description)
        VALUES (?, ?, ?)
        """,
        (patient_id, amount, description)
    )

    bill_id = cursor.lastrowid

    connection.commit()
    connection.close()

    print("\nBill created successfully!")
    print(f"Bill ID: {bill_id}")
    print(f"Patient: {patient['name']}")
    print(f"Amount: ₹{amount:.2f}")


def view_bills():
    """Display all bills."""

    print("\n========== BILLS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            b.bill_id,
            p.patient_id,
            p.name AS patient_name,
            b.amount,
            b.description
        FROM bills b
        JOIN patients p
            ON b.patient_id = p.patient_id
        ORDER BY b.bill_id
        """
    )

    bills = cursor.fetchall()

    connection.close()

    if not bills:
        print("No bills found.")
        return

    for bill in bills:

        print("\n------------------------------")
        print(f"Bill ID      : {bill['bill_id']}")
        print(f"Patient ID   : {bill['patient_id']}")
        print(f"Patient Name : {bill['patient_name']}")
        print(f"Amount       : ₹{bill['amount']:.2f}")
        print(f"Description  : {bill['description']}")