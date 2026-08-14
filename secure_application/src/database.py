import sqlite3
from pathlib import Path


# Path to the secure_application directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database file
DB_PATH = BASE_DIR / "hospital.db"


def get_connection():
    """Create and return a connection to the SQLite database."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create all required database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    # -------------------------
    # USERS TABLE
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # -------------------------
    # PATIENTS TABLE
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)

    # -------------------------
    # APPOINTMENTS TABLE
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_name TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            reason TEXT NOT NULL,
            FOREIGN KEY (patient_id)
                REFERENCES patients(patient_id)
        )
    """)

    # -------------------------
    # PRESCRIPTIONS TABLE
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_name TEXT NOT NULL,
            medicine TEXT NOT NULL,
            dosage TEXT NOT NULL,
            FOREIGN KEY (patient_id)
                REFERENCES patients(patient_id)
        )
    """)

    # -------------------------
    # BILLS TABLE
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (patient_id)
                REFERENCES patients(patient_id)
        )
    """)

    # -------------------------
    # MEDICAL RECORDS TABLE
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            diagnosis TEXT NOT NULL,
            treatment TEXT NOT NULL,
            record_file TEXT,
            FOREIGN KEY (patient_id)
                REFERENCES patients(patient_id)
        )
    """)

    # -------------------------
    # DEMO USERS
    # -------------------------

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password, role)
        VALUES ('admin', 'admin123', 'admin')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password, role)
        VALUES ('doctor', 'doctor123', 'doctor')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password, role)
        VALUES ('patient1', 'patient123', 'patient')
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully.")