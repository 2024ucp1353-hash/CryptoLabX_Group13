# Secure Application - Hospital Management System

**Course**: Cryptography Laboratory (22CPP307)  
**Assignment**: Lab Assignment 3  
**Application**: Hospital Management System (Group 13)  
**Team Members**:  
- **Ayush Sthapak** (2024UCP1353)  
- **Rishika Vijay** (2024UCP1398)  

---

## 📌 Application Overview

This project implements a console-based **Hospital Management System** as specified in Lab Assignment 3 ($13 \pmod{10} = 3$).

### Core Functionalities
1. **Authentication (`auth.py`)**: User authentication with SQLite database storage (`users` table).
2. **Patient Management (`patients.py`)**: Patient registration and directory listing.
3. **Appointment Management (`appointments.py`)**: Appointment scheduling and viewings.
4. **Prescription Management (`prescriptions.py`)**: Adding and viewing patient prescriptions.
5. **Billing (`billing.py`)**: Creating and displaying patient bills.
6. **Medical Records (`medical_records.py`)**: Medical record management.

---

## 📁 Repository Structure

```text
secure_application/
├── src/
│   ├── main.py                # Main CLI Application entry point
│   ├── database.py            # SQLite database initialization & tables
│   ├── auth.py                # Authentication module
│   ├── patients.py            # Patient registration & views
│   ├── appointments.py        # Appointment management
│   ├── prescriptions.py       # Prescription management
│   ├── billing.py             # Patient billing management
│   ├── medical_records.py     # Medical record management
│   ├── vulnerable_search.py   # Vulnerability 1: SQL Injection
│   ├── vulnerable_records.py  # Vulnerability 2: Broken Access Control
│   ├── vulnerable_files.py    # Vulnerability 3: Path Traversal
│   ├── patched_search.py      # Fix 1: Parameterized SQL query
│   ├── patched_records.py     # Fix 2: Role-based access control
│   └── patched_files.py       # Fix 3: Path sanitization & boundary check
├── testcases/                 # Exploit test scripts (test_sqli, test_broken_access, test_path_traversal)
├── sast/                      # Bandit SAST scan report (bandit_report.txt)
├── reports/                   # Security report (vulnerability_report.md)
├── screenshots/               # Exploits & SAST execution screenshots
└── README.md                  # Secure application documentation
```

---

## 🔒 3 Implemented Vulnerabilities & Fixes

1. **SQL Injection (SQLi)**:
   - *Vulnerable*: `vulnerable_search.py` (String concatenation in SQL queries)
   - *Fix*: `patched_search.py` (Parameterized query execution)
2. **Broken Access Control (BAC)**:
   - *Vulnerable*: `vulnerable_records.py` (Missing role verification)
   - *Fix*: `patched_records.py` (Role-based access control checks)
3. **Path Traversal**:
   - *Vulnerable*: `vulnerable_files.py` (Unsanitized filename join with `../`)
   - *Fix*: `patched_files.py` (`os.path.basename` & directory boundary checks)

---

## 🛠️ How to Run & Test

### Run Main Hospital App
```bash
python3 secure_application/src/main.py
```

### Run Security Exploit Tests
```bash
python3 secure_application/testcases/test_sqli.py
python3 secure_application/testcases/test_broken_access.py
python3 secure_application/testcases/test_path_traversal.py
```

### Run Bandit SAST Scan
```bash
bandit -r secure_application/src/ -f txt -o secure_application/sast/bandit_report.txt
```
