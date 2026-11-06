# OS Random Number Generation & Statistical Evaluation

**Course**: Cryptography Laboratory (22CPP307)  
**Academic Year**: 2026  
**Assignment**: Operating System Random Number Generation and Statistical Security Analysis  

---

## 👥 Authors (Group 13)

- **Ayush Sthapak** (2024UCP1353)
- **Rishika Vijay** (2024UCP1398)

---

## 🎯 Objective

Evaluate operating-system random-number generation mechanisms across Linux and Windows, generate 1 MiB binary samples from each CSPRNG, apply comprehensive statistical test batteries (Serial Correlation, Pearson's Chi-Square, NIST SP 800-22 Monobit and Runs tests), and investigate the mathematical boundary between **statistical randomness** and **cryptographic security**.

---

## 📁 Repository & Directory Layout

```text
OS_Random_Number_Generation/
├── data/
│   ├── linux_urandom.bin       # 1 MiB generated via Linux /dev/urandom
│   ├── openssl_rand.bin        # 1 MiB generated via OpenSSL rand
│   └── windows_cng.bin         # 1 MiB generated via Windows CNG / .NET
├── plots/
│   ├── byte_distribution.png   # Byte-frequency distribution charts
│   └── bit_distribution.png    # 0s vs 1s bit-count comparative chart
├── generate_linux.sh           # Bash generation script for Linux /dev/urandom & OpenSSL
├── generate_windows.ps1         # PowerShell generation script for Windows CNG / .NET
├── statistical_tests.py        # Advanced statistical test suite CLI engine
├── Random_Number_Analysis.ipynb # Comprehensive interactive Jupyter Notebook
├── Linux_RNG_Research.md       # In-depth architectural report on Linux CSPRNG
├── Windows_RNG_Research.md     # In-depth architectural report on Windows CNG
├── Security_Comparison.md      # Security comparison & why statistical tests != security
└── README.md                   # Lab execution documentation & results report
```

---

## 🚀 How to Execute & Reproduce

### 1. Generating Datasets

#### On Linux / macOS:
```bash
chmod +x generate_linux.sh
./generate_linux.sh
```

#### On Windows (PowerShell):
```powershell
.\generate_windows.ps1
```

### 2. Running the Statistical Test Suite (CLI)
```bash
python3 statistical_tests.py
```

### 3. Interactive Jupyter Notebook
```bash
jupyter notebook Random_Number_Analysis.ipynb
```

---

## 📊 Experimental Results

Across all three $1\text{ MiB}$ binary datasets ($N = 1,048,576\text{ bytes} = 8,388,608\text{ bits}$), the experimental results are summarized below:

| Statistical Metric | Expected Ideal Value | Linux `/dev/urandom` | OpenSSL `rand` | Windows CNG (`.NET`) |
| :--- | :--- | :--- | :--- | :--- |
| **File Size (Bytes)** | $1,048,576$ | $1,048,576$ | $1,048,576$ | $1,048,576$ |
| **Serial Correlation ($r$)** | $\approx 0.000000$ | $+0.001351$ | $-0.001786$ | $+0.000099$ |
| **Chi-Square $\chi^2$ ($df=255$)** | $\approx 255.0$ | $300.66$ | $266.26$ | $207.84$ |
| **Chi-Square $P$-value** | $\ge 0.01$ | $0.0261$ (PASS) | $0.3013$ (PASS) | $0.9862$ (PASS) |
| **Bit Distribution (0s / 1s)** | $50.00\% / 50.00\%$ | $50.02\% / 49.98\%$ | $50.01\% / 49.99\%$ | $50.01\% / 49.99\%$ |
| **NIST Monobit $S_{obs}$** | Close to $0.0$ | $1.4322$ | $0.7665$ | $0.8259$ |
| **NIST Monobit $P$-value** | $\ge 0.01$ | $0.1521$ (PASS) | $0.4434$ (PASS) | $0.4089$ (PASS) |
| **NIST Runs Observed** | $\approx 4,194,304$ | $4,196,011$ | $4,193,947$ | $4,192,779$ |
| **NIST Runs $P$-value** | $\ge 0.01$ | $0.2382$ (PASS) | $0.8054$ (PASS) | $0.2924$ (PASS) |
| **Overall Verdict** | All $P \ge 0.01$ | **PASS** | **PASS** | **PASS** |

---

## 🔬 Key Security Takeaways

1. **Both Linux and Windows implement robust CSPRNGs**: Linux's ChaCha20 kernel generator and Windows's NIST SP 800-90A AES-CTR DRBG provide forward secrecy, backtracking resistance, and high-throughput entropy mixing.
2. **Statistical Randomness $\neq$ Cryptographic Security**:
   - Statistical batteries (NIST SP 800-22, Chi-Square, Runs) only assess empirical output distribution (absence of linear bias or trivial repetition).
   - Insecure generators such as Mersenne Twister (MT19937) and fixed-key counter-mode AES easily achieve passing statistical scores while being completely predictable.
   - True cryptographic security requires computational next-bit unpredictability and protection against state inversion.
