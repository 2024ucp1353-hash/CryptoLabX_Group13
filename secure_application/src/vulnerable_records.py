from database import get_connection


def view_record_vulnerable(user_role: str):
    """Vulnerability 2: Broken Access Control (BAC)
    Fails to enforce role-based access control. Any user (including lower-privileged
    patients) can view sensitive medical diagnosis and treatment history of any patient.
    """
    print("\n========== VIEW MEDICAL RECORD (VULNERABLE: BAC) ==========")
    print(f"Logged in user role: {user_role}")
    
    # VULNERABILITY: Missing authorization check! No check for user_role == 'admin' or 'doctor'
    record_id = input("Enter Record ID to view: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT mr.record_id, p.name AS patient_name, mr.diagnosis, mr.treatment, mr.record_file
        FROM medical_records mr
        JOIN patients p ON mr.patient_id = p.patient_id
        WHERE mr.record_id = ?
    """

    cursor.execute(query, (record_id,))
    record = cursor.fetchone()
    connection.close()

    if record:
        print("\n[CONFIDENTIAL MEDICAL RECORD ACCESSED]")
        print(f"Record ID    : {record['record_id']}")
        print(f"Patient Name : {record['patient_name']}")
        print(f"Diagnosis    : {record['diagnosis']}")
        print(f"Treatment    : {record['treatment']}")
        print(f"File Path    : {record['record_file']}")
    else:
        print("Record not found.")
