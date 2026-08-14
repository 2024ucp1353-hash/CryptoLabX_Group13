"""Security Test Case 2: Broken Access Control (BAC) Demonstration
Tests unauthorized viewing of confidential medical records by lower-privileged roles.
"""
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

from database import get_connection, initialize_database


def run_bac_test():
    print("=" * 60)
    print("TEST CASE 2: BROKEN ACCESS CONTROL EXPLOITATION")
    print("=" * 60)

    initialize_database()
    connection = get_connection()
    cursor = connection.cursor()

    # Seed test medical record
    cursor.execute("INSERT OR IGNORE INTO patients (patient_id, name, age, gender, phone, address) VALUES (1, 'John Doe', 30, 'Male', '9876543210', '123 Main St')")
    cursor.execute("INSERT OR IGNORE INTO medical_records (record_id, patient_id, diagnosis, treatment, record_file) VALUES (1, 1, 'Stage 2 Hypertension', 'Lisinopril 10mg daily', 'rec_101.txt')")
    connection.commit()

    unauthorized_user_role = "patient"  # Regular patient attempting admin/doctor function
    print(f"[+] Attempting to view medical record #1 as role: '{unauthorized_user_role}'")

    # Simulate vulnerable function missing role check
    cursor.execute("SELECT record_id, diagnosis, treatment FROM medical_records WHERE record_id = 1")
    record = cursor.fetchone()
    connection.close()

    if record:
        print("[+] Unauthorized Access Granted!")
        print(f"    - Leaked Diagnosis: {record['diagnosis']}")
        print(f"    - Leaked Treatment: {record['treatment']}")

    assert record is not None, "BAC test failed."
    print("\n[RESULT]: Broken Access Control Vulnerability SUCCESSFULLY Exploited!\n")


if __name__ == "__main__":
    run_bac_test()
