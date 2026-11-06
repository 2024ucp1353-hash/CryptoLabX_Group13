
# 512-Bit Prime Generation Using Miller-Rabin Primality Test

## 1. Aim
To generate a cryptographically strong probable prime number of exactly 512 bits using the Miller-Rabin probabilistic primality testing algorithm.

## 2. Objectives
- Generate random odd 512-bit candidates.
- Implement fast modular exponentiation.
- Implement the Miller-Rabin primality test.
- Generate a probable prime by rejecting composite candidates.
- Count the number of candidates tested.
- Measure the execution time.
- Independently verify the generated prime using SymPy.

## 3. Technologies Used
- Python 3
- secrets module for cryptographically secure random number generation
- time module for execution-time measurement
- SymPy for independent primality verification

## 4. Algorithm

1. Generate a random 512-bit integer using a cryptographically secure random generator.
2. Set its most significant bit to ensure exactly 512 bits.
3. Set its least significant bit to ensure the candidate is odd.
4. Express n - 1 as 2^s * d, where d is odd.
5. Select random bases and perform Miller-Rabin witness tests.
6. Reject the candidate if it is composite.
7. Repeat until a probable prime is found.
8. Record the number of candidates tested and execution time.
9. Verify the result independently using SymPy.

## 5. Execution Instructions

Clone the repository:

```bash
git clone https://github.com/2024ucp1353-hash/CryptoLabX_Group13.git
```

Navigate to the assignment directory:

```bash
cd CryptoLabX_Group13/Miller_Rabin
```

Install the required dependency:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python miller_rabin.py
```

## 6. Experimental Parameters

| Parameter | Value |
|---|---|
| Assigned bit length | 512 |
| Miller-Rabin rounds | 40 |
| Candidate generation | Cryptographically secure |
| Independent verification | SymPy |

## 7. Experimental Results

The program displays:
- Generated probable prime
- Actual bit length
- Number of candidates tested
- Number of Miller-Rabin rounds
- Total execution time
- Independent primality verification result

The actual values are generated and displayed when the program is executed.

## 8. Verification

The generated number is checked using:
1. Its bit length must be exactly 512.
2. It must pass the implemented Miller-Rabin test.
3. It must pass the independent SymPy primality check.

## 9. Conclusion

A probable prime number of exactly 512 bits is generated using the Miller-Rabin primality testing algorithm. The experiment records candidate count and execution time and independently verifies the generated result using SymPy.
