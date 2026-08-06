# CryptoLabA2 - Cryptography Laboratory Toolkit

**Course**: Cryptography Laboratory (22CPP307)  
**Assignment**: Assignment 1 (Week 1) - Build Your CryptoLabA2 Toolkit  
**Repository**: `CryptoLabA2_Group13`

---

## 📌 Project Overview

**CryptoLabA2** is a modular python-based cryptanalysis and cryptography software framework developed as part of the Cryptography Laboratory course. This toolkit serves as a foundation for building, testing, and evaluating classical and modern cryptographic ciphers, cryptanalysis attacks, mathematical operations, and statistical frequency analysis.

Week 1 establishes the clean project architecture, command-line interface, file analysis engine, text datasets, and automated execution logging system.

---

## 👥 Team Members

- **Ayush Sthapak** (2024UCP1353)
- **Rishika Vijay** (2024UCP1398)

---

## 📁 Directory Structure & Architecture

```text
CryptoLabA2/
├── classical/      # Implementations of classical ciphers (Caesar, Vigenere, Playfair, Hill, etc.)
├── attacks/        # Cryptanalysis attack algorithms (Frequency analysis, Brute force, Kasiski)
├── math/           # Mathematical helper utilities (GCD, Modular Inverse, Matrix Ops, Primes)
├── modern/         # Modern symmetric/asymmetric cipher implementations (AES, DES, RSA, ECC)
├── analysis/       # Statistical and frequency analysis utilities
├── datasets/       # Input plaintexts and ciphertexts for testing (contains sample1 - sample5)
├── outputs/        # Output logs, decrypted results, and analysis artifacts (execution.log)
├── docs/           # Documentation, lab reports, and reference guides
├── tests/          # Unit tests and validation scripts for all modules
├── utils/          # Core utilities (file_analysis.py, logger.py)
├── main.py         # Main entry point - Interactive CLI application
├── README.md       # Project documentation
└── requirements.txt# Project Python dependencies
```

### Directory Details

- **`classical/`**: Holds future modules for historical substitution and transposition ciphers.
- **`attacks/`**: Reserved for automated ciphertext-only, known-plaintext, and chosen-plaintext attack tools.
- **`math/`**: Contains core number theory and modular arithmetic routines required for cryptographic operations.
- **`modern/`**: Reserved for modern block ciphers, stream ciphers, and public-key cryptosystems.
- **`analysis/`**: Holds entropy calculations, index of coincidence, and n-gram analysis tools.
- **`datasets/`**: Includes text files (`sample1.txt` to `sample5.txt`) for empirical testing.
- **`outputs/`**: Stores execution history logs (`outputs/execution.log`) and output artifacts.
- **`utils/`**: Houses utility logic including `file_analysis.py` and `logger.py`.

---

## 🚀 Features (Assignment 1)

1. **Interactive Menu-Driven CLI (`main.py`)**:
   - `1. Encrypt` - Placeholder for cipher encryption engines (Coming Soon).
   - `2. Decrypt` - Placeholder for cipher decryption engines (Coming Soon).
   - `3. Attack` - Placeholder for cryptanalysis attack routines (Coming Soon).
   - `4. Analyze` - Interactively inspects and analyzes text files from `datasets/`.
   - `5. Exit` - Gracefully exits the application.

2. **File Analysis Engine (`utils/file_analysis.py`)**:
   Calculates key text metrics for any dataset file:
   - Total character count
   - Total word count
   - Total line count
   - Unique character count
   - Full alphabetical letter frequency distribution

3. **Automated Logging System (`utils/logger.py`)**:
   - Automatically logs every execution event into `outputs/execution.log`.
   - Records exact date, timestamp (`YYYY-MM-DD HH:MM:SS`), and selected menu options.

4. **Cryptographic Datasets (`datasets/`)**:
   - `sample1.txt`: Introductory plaintext sample.
   - `sample2.txt`: Caesar cipher ciphertext sample.
   - `sample3.txt`: Monoalphabetic substitution ciphertext sample.
   - `sample4.txt`: Columnar transposition sample.
   - `sample5.txt`: Historical cryptography essay text.

---

## ⚙️ How to Run

### Prerequisites

- Python 3.8 or higher installed on your system.

### Running the Toolkit

Run `main.py` directly from the project root directory:

```bash
python3 main.py
```

### Example Usage (File Analysis)

1. Launch `python3 main.py`.
2. Select Option `4` (**Analyze**).
3. Enter the filename when prompted (e.g., `sample1.txt` or `sample2.txt`).
4. View the character, word, line counts, and letter frequency table.

---

## 🗺️ Future Modules & Roadmap

- **Week 2**: Classical Substitution Ciphers (Caesar, Monoalphabetic, Polyalphabetic/Vigenère).
- **Week 3**: Transposition Ciphers (Rail Fence, Columnar Transposition).
- **Week 4**: Automated Cryptanalysis (Index of Coincidence, Kasiski Examination, Frequency Analysis).
- **Week 5+**: Modern Cryptosystems (DES, AES, RSA, Diffie-Hellman Key Exchange) & Mathematical Utilities.

---

_CryptoLabA2 Toolkit - Cryptography Laboratory (22CPP307)_
