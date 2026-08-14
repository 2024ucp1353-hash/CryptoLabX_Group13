# CryptoLab - Cryptography Laboratory Toolkit

**Course**: Cryptography Laboratory (22CPP307)  
**Repository**: `CryptoLabX_Group13`  

---

## 👥 Team Members

- **Ayush Sthapak** (2024UCP1353)
- **Rishika Vijay** (2024UCP1398)

---

## 📁 Repository Structure & Architecture

```text
CryptoLab/
├── classical/            # Historical ciphers (Caesar, Vigenère, Playfair, Hill)
├── modern/               # Modern symmetric & asymmetric algorithms (AES, DES, RSA)
├── hashing/              # Cryptographic hash functions (MD5, SHA-256)
├── attacks/              # Cryptanalysis attack tools (Brute force, Frequency analysis)
├── analysis/             # Statistical analysis routines
├── docs/                 # Documentation and guides
├── datasets/             # Text corpora & ciphertexts for analysis (sample1 - sample5)
├── outputs/              # Output logs and execution artifacts (execution.log)
├── utils/                # Core utilities (file_analysis.py, logger.py)
├── main.py               # CryptoLab CLI Toolkit Entry Point
│
└── secure_application/   # Lab Assignment 3: Hospital Management System
    ├── src/              # Application source code & vulnerability/patch modules
    ├── reports/          # Security analysis reports (vulnerability_report.md)
    ├── screenshots/      # Exploit & SAST verification screenshots
    ├── sast/             # Bandit SAST scan report (bandit_report.txt)
    ├── testcases/        # Automated security exploit scripts
    └── README.md         # Secure application documentation
```

---

## 📌 Assignments Overview

### 1. Assignment 1: CryptoLab Toolkit Foundation
- **Interactive Menu CLI (`main.py`)**: Supports encryption, decryption, attack, analysis, and exit options.
- **File Analysis Engine (`utils/file_analysis.py`)**: Calculates character, word, line counts, unique characters, and letter frequency distributions.
- **Execution Logger (`utils/logger.py`)**: Logs date, time, and menu selection events into `outputs/execution.log`.
- **Datasets Corpus (`datasets/`)**: Contains sample text datasets (`sample1.txt` to `sample5.txt`).

### 2. Lab Assignment 3: Secure Application (Hospital Management System)
Located inside [`secure_application/`](secure_application/README.md):
- **Core Functionalities**: Authentication, Patient Registration, Appointments, Prescriptions, Billing, and Medical Records.
- **3 Implemented Vulnerabilities**:
  1. SQL Injection (`vulnerable_search.py`)
  2. Broken Access Control (`vulnerable_records.py`)
  3. Path Traversal (`vulnerable_files.py`)
- **Bandit SAST Analysis**: Automated security scan output saved in `secure_application/sast/bandit_report.txt`.
- **Security Exploit Test Cases**: Automated test scripts in `secure_application/testcases/`.
- **Vulnerability Remediations**: Patched modules in `secure_application/src/` (`patched_search.py`, `patched_records.py`, `patched_files.py`).

---

## 🚀 How to Run & Test

### Running CryptoLab Toolkit (Assignment 1)
```bash
python3 main.py
```

### Running Hospital Management System (Lab Assignment 3)
```bash
python3 secure_application/src/main.py
```

### Running Security Exploit Test Suite
```bash
python3 secure_application/testcases/test_sqli.py
python3 secure_application/testcases/test_broken_access.py
python3 secure_application/testcases/test_path_traversal.py
```

### Running Bandit SAST Scanner
```bash
bandit -r secure_application/src/ -f txt -o secure_application/sast/bandit_report.txt
```

---

*CryptoLab Toolkit - Cryptography Laboratory (22CPP307)*
