# CryptoLab - Cryptography Laboratory Toolkit

**Course**: Cryptography Laboratory (22CPP307)  
**Repository**: `CryptoLabX_Group13`  
**Academic Year**: 2026

---

## 👥 Team Members (Group 13)

- **Ayush Sthapak** (2024UCP1353)
- **Rishika Vijay** (2024UCP1398)

---

## 📁 Repository Structure & Architecture

```text
CryptoLabX_Group13/
├── main.py                     # CryptoLab CLI Toolkit Entry Point (Assignment 1)
├── datasets/                   # Sample text datasets (sample1.txt to sample5.txt)
├── utils/                      # Core utilities (file_analysis.py, logger.py)
├── outputs/                    # Execution logs (execution.log)
├── requirements.txt            # Python dependencies
│
├── attacks/
│   ├── shift_cipher_attack/    # Assignment 4: Shift Cipher Cryptanalysis
│   │   ├── src/
│   │   │   ├── shift_cipher.py           # Core Shift Cipher (Encrypt/Decrypt)
│   │   │   ├── brute_force_dictionary.py # Brute-force with Dictionary Scoring
│   │   │   ├── chi_square_attack.py      # Statistical Chi-Square Analysis
│   │   │   └── main.py                   # Automated Cryptanalysis Pipeline
│   │   ├── dictionary/
│   │   │   └── english_words.txt         # Wordlist for dictionary scoring
│   │   ├── testcases/                    # Shift cipher test cases (testcase1 - testcase3)
│   │   ├── outputs/                      # Attack execution output logs
│   │   └── screenshots/                  # Execution screenshots (output.png)
│   │
│   ├── monoalphabetic_cipher/  # Assignment 5: Monoalphabetic Substitution Cipher
│   │   ├── main.cpp                      # C++ Frequency & Pattern Cryptanalysis Engine
│   │   ├── plaintext.txt                 # Source text (Katz & Lindell, Page 43)
│   │   └── ciphertext.txt                # Encrypted ciphertext output
│   │
│   └── vigenere_cipher/        # Assignment 6: Vigenère Cipher Cryptanalysis
│       ├── src/
│       │   └── vigenere_cryptanalysis.py # Kasiski & IC Cryptanalysis Pipeline
│       └── ciphertext/
│           └── ciphertext.txt            # Assigned polyalphabetic ciphertext (Odd Group 13)
│
└── secure_application/         # Assignment 2 & 3: SAST Tools & Secure Application (HMS)
    ├── src/                    # HMS source code, vulnerable & patched modules
    ├── testcases/              # Automated security exploit scripts (SQLi, BAC, Path Traversal)
    ├── sast/                   # Automated Bandit SAST scan report (bandit_report.txt)
    ├── reports/                # Security vulnerability analysis report
    ├── screenshots/            # Exploit & scan screenshots
    └── README.md               # Secure application documentation
```

---

## 📌 Laboratory Assignments Overview

---

### 1. Lab Assignment 1: CryptoLab Toolkit Foundation
- **Interactive CLI (`main.py`)**: Menu-driven interface providing encryption, decryption, cryptanalysis, file analysis, and logging operations.
- **File Analysis Engine (`utils/file_analysis.py`)**: Computes character counts, word counts, line counts, unique character statistics, and letter frequency distributions.
- **Execution Logger (`utils/logger.py`)**: Automatically records timestamped user interactions and menu executions into `outputs/execution.log`.
- **Text Corpus (`datasets/`)**: Benchmark text samples (`sample1.txt` to `sample5.txt`) for cryptographic benchmarking.

---

### 2. Lab Assignment 2 & 3: Static Application Security Testing (SAST) & Secure Application
Located in [`secure_application/`](secure_application/README.md):
- **Assigned Tool**: **Bandit** (Assigned for Group 13: Tool 1) for automated static security analysis of Python code.
- **Application**: Hospital Management System (HMS) console application with authentication, patient records, appointments, prescriptions, and billing.
- **3 Vulnerability & Remediation Pairs**:
  1. **SQL Injection**: `vulnerable_search.py` $\to$ Fixed with parameterized queries in `patched_search.py`.
  2. **Broken Access Control**: `vulnerable_records.py` $\to$ Fixed with role-based access checks (RBAC) in `patched_records.py`.
  3. **Path Traversal**: `vulnerable_files.py` $\to$ Fixed with filename sanitization and directory restriction in `patched_files.py`.
- **Automated Exploit Suite**: Python test harnesses in `secure_application/testcases/` demonstrating exploits before remediation.
- **SAST Security Auditing**: Automated static code analysis scan using Bandit with findings and rule IDs documented in `secure_application/sast/bandit_report.txt`.

---

### 3. Lab Assignment 4: Shift Cipher Cryptanalysis
Located in [`attacks/shift_cipher_attack/`](attacks/shift_cipher_attack/):
- **Cipher Engine (`shift_cipher.py`)**: Implements shift encryption and decryption with case and symbol preservation.
- **Dictionary Scoring Attack (`brute_force_dictionary.py`)**: Tests all 26 shift keys against an English dictionary (`dictionary/english_words.txt`), selecting the candidate that maximizes valid English word matches.
- **Chi-Square ($\chi^2$) Analysis (`chi_square_attack.py`)**: Measures goodness-of-fit against standard English unigram letter frequencies:
  $$\chi^2 = \sum_{i='a'}^{'z'} \frac{(O_i - E_i)^2}{E_i}$$
  The shift key yielding the minimum $\chi^2$ value is selected as the recovered key without requiring word boundaries or dictionary lookups.
- **Automated Pipeline (`main.py`)**: Runs both attack techniques side-by-side on encrypted ciphertexts and outputs comparative performance metrics.

---

### 4. Lab Assignment 5: Monoalphabetic Substitution Cipher Cryptanalysis
Located in [`attacks/monoalphabetic_cipher/`](attacks/monoalphabetic_cipher/):
- **Language**: Standard C++ (`main.cpp`) without external cryptanalysis libraries.
- **Dataset**: Plaintext selected from *Modern Cryptography* by Katz and Lindell (Page $(\text{Group } 13 + 30) = 43$, Chapter 3: Private-Key Encryption).
- **Cryptanalysis Workflow**:
  1. **Letter Frequency Analysis (`frequency_analysis`)**: Counts, sorts, and calculates percentage frequencies for all 26 ciphertext letters.
  2. **Word Frequency Analysis (`word_frequency_analysis`)**: Identifies 1-letter words (`Q` $\to$ `A`), 2-letter words (`OF`, `VT`, `GY`, `ZG`, `OL`), 3-letter words (`ZIT` $\to$ `THE`), and repeated words.
  3. **Pattern Analysis (`pattern_analysis`)**: Extracts isomorphic word patterns (e.g. `HTKYTEZ` $\to$ `PERFECT`, `LTEKTEN` $\to$ `SECRECY`, `EKNHZGUKQHIN` $\to$ `CRYPTOGRAPHY`).
  4. **Iterative Recovery (`apply_substitution`, `display_partial_plaintext`)**: Step-by-step hypothesis testing displaying unrecovered letters as `_` with real-time recovery progress percentage.
  5. **Solution Verification (`verify_solution`)**: Recovers key `QWERTYUIOPASDFGHJKLZXCVBNM`, re-encrypts plaintext, and verifies a 100% exact match against original ciphertext.

---

### 5. Lab Assignment 6: Vigenère Cipher Cryptanalysis
Located in [`attacks/vigenere_cipher/`](attacks/vigenere_cipher/):
- **Assigned Ciphertext**: Ciphertext 1 (Odd Group No. — Group 13), 395 characters.
- **Cryptanalysis Workflow**:
  1. **Ciphertext Preprocessing (`clean_ciphertext`)**: Normalizes ciphertext and strips non-alphabetic symbols.
  2. **Kasiski Examination (`find_repeated_patterns`, `calculate_distances`, `find_factors`, `kasiski_analysis`)**: Finds repeated polyalphabetic n-grams, calculates spacing distances, and determines candidate key lengths (identifying length 14).
  3. **Index of Coincidence (`calculate_ic`, `calculate_average_ic`)**: Evaluates average IC across candidate key lengths $1 \dots 20$, confirming key length $14$ ($\text{IC} = 0.0644 \approx 0.067$ English standard).
  4. **Coset Group Splitting (`split_into_groups`)**: Splits ciphertext into 14 monoalphabetic sub-streams.
  5. **Caesar Shift Detection & Key Recovery (`frequency_analysis`, `find_shift`, `find_key`)**: Applies Chi-Square goodness-of-fit to each coset group to recover the 14-letter key: **`AMBROISETHOMAS`**.
  6. **Decryption & Verification (`vigenere_decrypt`, `vigenere_encrypt`, `verify`)**: Decrypts the ciphertext to full English plaintext and verifies re-encryption match.

---

## 🚀 How to Run & Test

### 1. Assignment 1: CryptoLab Toolkit CLI
```bash
python3 main.py
```

### 2. Lab Assignment 2 & 3: Hospital Management System & Security Exploits (SAST - Bandit)
```bash
# Run application
python3 secure_application/src/main.py

# Run automated exploit test suite
python3 secure_application/testcases/test_sqli.py
python3 secure_application/testcases/test_broken_access.py
python3 secure_application/testcases/test_path_traversal.py

# Run Bandit SAST security scanner
bandit -r secure_application/src/ -f txt -o secure_application/sast/bandit_report.txt
```

### 3. Lab Assignment 4: Shift Cipher Cryptanalysis
```bash
# Run full automated attack pipeline
python3 attacks/shift_cipher_attack/src/main.py

# Run individual attack modules
python3 attacks/shift_cipher_attack/src/shift_cipher.py
python3 attacks/shift_cipher_attack/src/brute_force_dictionary.py
python3 attacks/shift_cipher_attack/src/chi_square_attack.py
```

### 4. Lab Assignment 5: Monoalphabetic Substitution Cryptanalysis (C++)
```bash
# Compile and run
cd attacks/monoalphabetic_cipher
g++ -std=c++17 main.cpp -o main
./main
```

### 5. Lab Assignment 6: Vigenère Cipher Cryptanalysis (Python)
```bash
# Run Kasiski examination & automated frequency cryptanalysis
cd attacks/vigenere_cipher
python3 src/vigenere_cryptanalysis.py
```

---

*CryptoLabX - Group 13 | Department of Computer Science & Engineering | MNIT Jaipur*
