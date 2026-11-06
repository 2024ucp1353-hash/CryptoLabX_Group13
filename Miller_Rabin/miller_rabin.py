"""
Cryptography Laboratory (22CPP307) - Assignment 8
Cryptographic Prime Generation Using Miller–Rabin Primality Test

Group 13:
- Ayush Sthapak (2024UCP1353)
- Rishika Vijay (2024UCP1398)

Commit 1: Setup project structure and input handling
- Create the Python file/notebook structure.
- Import required libraries.
- Set the assigned bit length to 512.
- Handle random odd candidate generation.

Commit 2: Implement modular exponentiation
- Implement fast modular exponentiation (Square-and-Multiply).
- Calculate a^d mod n efficiently for large integers.
- Handle large 512-bit integers without memory overhead or integer overflow.
"""

import secrets
import random
import sys

# ==============================================================================
# Configuration & Assigned Parameters
# ==============================================================================
# Assigned bit length for cryptographic prime generation
BIT_LENGTH = 512


# ==============================================================================
# Commit 1: Input Handling & Random Odd Candidate Generation
# ==============================================================================
def generate_odd_candidate(bit_length: int = BIT_LENGTH) -> int:
    """
    Generates a cryptographically strong random odd integer candidate
    of exactly the specified bit length.

    Properties guaranteed:
    1. Bit length is exactly `bit_length` (Most Significant Bit is set to 1).
    2. Number is odd (Least Significant Bit is set to 1, eliminating even composites).
    3. Intermediate bits are generated using cryptographically secure randomness.

    Args:
        bit_length: Desired bit length (default: 512 bits).

    Returns:
        int: An odd integer candidate with exactly `bit_length` bits.
    """
    if bit_length < 2:
        raise ValueError("Bit length must be at least 2 for prime candidates.")

    # Generate random integer of bit_length bits using secrets (CSPRNG)
    candidate = secrets.randbits(bit_length)

    # Ensure the most significant bit (MSB) is set so the number has exactly bit_length bits
    candidate |= (1 << (bit_length - 1))

    # Ensure the least significant bit (LSB) is set so the number is odd
    candidate |= 1

    return candidate


def validate_candidate_properties(candidate: int, expected_bits: int = BIT_LENGTH) -> bool:
    """
    Validates that a generated candidate has the exact expected bit length
    and is an odd integer.

    Args:
        candidate: The integer candidate to validate.
        expected_bits: Expected bit length (default: 512).

    Returns:
        bool: True if candidate matches both bit length and odd parity constraints.
    """
    is_odd = (candidate % 2 == 1)
    has_exact_bits = (candidate.bit_length() == expected_bits)
    return is_odd and has_exact_bits


# ==============================================================================
# Commit 2: Fast Modular Exponentiation (Square-and-Multiply)
# ==============================================================================
def modular_exponentiation(base: int, exponent: int, modulus: int) -> int:
    """
    Computes (base^exponent) mod modulus using the Square-and-Multiply algorithm
    (binary exponentiation).

    This efficiently calculates a^d mod n for large 512-bit integers in O(log exponent)
    time, avoiding the computation of astronomical intermediate values by reducing
    modulo `modulus` at every multiplication step.

    Algorithm:
    1. Initialize result = 1.
    2. Reduce base modulo modulus: base = base % modulus.
    3. While exponent > 0:
        a. If current lowest bit of exponent is 1 (exponent & 1):
           result = (result * base) % modulus
        b. Square the base:
           base = (base * base) % modulus
        c. Shift exponent right by 1 bit:
           exponent >>= 1
    4. Return result.

    Args:
        base: The base integer (a).
        exponent: The exponent integer (d >= 0).
        modulus: The positive modulus integer (n > 0).

    Returns:
        int: (base^exponent) % modulus.
    """
    if modulus <= 0:
        raise ValueError("Modulus must be a positive integer.")
    if modulus == 1:
        return 0
    if exponent < 0:
        raise ValueError("Negative exponents are not supported in integer modular arithmetic.")
    if exponent == 0:
        return 1

    result = 1
    base = base % modulus

    while exponent > 0:
        # If the lowest bit is set, multiply current base into result
        if exponent & 1:
            result = (result * base) % modulus
        # Square the base for the next bit position
        base = (base * base) % modulus
        # Shift exponent right by 1 bit
        exponent >>= 1

    return result


if __name__ == "__main__":
    print(f"[*] Assignment 8: Miller-Rabin Primality Test")
    print(f"[*] Assigned Bit Length: {BIT_LENGTH}")

    # Test Candidate Generation (Commit 1)
    sample_candidate = generate_odd_candidate(BIT_LENGTH)
    print(f"\n--- [Commit 1] Candidate Generation ---")
    print(f"[*] Sample Candidate ({sample_candidate.bit_length()} bits):")
    print(f"    {sample_candidate}")
    print(f"[*] Validated (Odd & Exactly {BIT_LENGTH} bits): "
          f"{validate_candidate_properties(sample_candidate, BIT_LENGTH)}")

    # Test Modular Exponentiation (Commit 2)
    print(f"\n--- [Commit 2] Fast Modular Exponentiation (Square-and-Multiply) ---")
    test_base = 2
    test_exp = 65537
    test_mod = sample_candidate
    calc_res = modular_exponentiation(test_base, test_exp, test_mod)
    expected_res = pow(test_base, test_exp, test_mod)
    print(f"[*] Calculating ({test_base}^{test_exp}) mod candidate...")
    print(f"    Computed Result: {calc_res}")
    print(f"    Correctness check vs built-in pow(): {calc_res == expected_res}")
