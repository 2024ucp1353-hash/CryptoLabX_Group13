from database import get_connection


def view_record_secure(user_role: str):
    """FIX 2: Broken Access Control Remediation
    Enforces Role-Based Access Control (RBAC). Only users with 'admin' or 'doctor'
    roles are authorized to view confidential medical records.
    """
    print("\n========== VIEW MEDICAL RECORD (SECURE: RBAC Enforced) ==========")
    print(f"Logged in user role: {user_role}")

    # SECURE: Strict role-based authorization check
    if user_role.lower() not in ["admin", "doctor"]:
        print("\n[ACCESS DENIED]: You do not have permission to view confidential medical records.")
        return

    record_id = input("Enter Record ID to view: ").strip()

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
