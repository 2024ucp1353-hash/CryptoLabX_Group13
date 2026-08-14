from database import get_connection


def search_patients_secure():
    """FIX 1: SQL Injection Remediation
    Uses parameterized SQL queries with tuple placeholders (?) to prevent SQL injection.
    Input sanitization & parameterization ensures search terms are treated strictly as literals.
    """
    print("\n========== SEARCH PATIENTS (SECURE: Parameterized Query) ==========")
    search_term = input("Enter patient name to search: ").strip()

    if not search_term:
        print("Search term cannot be empty.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    # SECURE: Parameterized SQL query prevents SQL Injection
    query = """
        SELECT patient_id, name, age, gender, phone, address
        FROM patients
        WHERE name LIKE ?
    """
    cursor.execute(query, (f"%{search_term}%",))
    results = cursor.fetchall()

    if not results:
        print("No matching patients found.")
    else:
        for patient in results:
            print(f"ID: {patient['patient_id']} | Name: {patient['name']} | Phone: {patient['phone']}")

    connection.close()
