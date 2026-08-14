from database import get_connection

# Hardcoded secret for SAST demonstration (Bandit B105)
API_SECRET_KEY = "hospital_admin_secret_key_12345"


def search_patients_vulnerable():
    """Vulnerability 1: SQL Injection (SQLi)
    Uses direct string interpolation inside cursor.execute to construct SQL queries.
    Vulnerable payload example: ' OR '1'='1
    """
    print("\n========== SEARCH PATIENTS (VULNERABLE: SQLi) ==========")
    search_term = input("Enter patient name to search: ")

    connection = get_connection()
    cursor = connection.cursor()

    # VULNERABLE SQL QUERY (Bandit B608): String concatenation in cursor.execute allows SQL Injection
    cursor.execute(f"SELECT patient_id, name, age, gender, phone, address FROM patients WHERE name LIKE '%" + search_term + "%'")
    results = cursor.fetchall()

    if not results:
        print("No matching patients found.")
    else:
        for patient in results:
            print(f"ID: {patient['patient_id']} | Name: {patient['name']} | Phone: {patient['phone']}")

    connection.close()
