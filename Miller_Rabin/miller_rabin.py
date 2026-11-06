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

Commit 3: Implement Miller–Rabin primality test
- Factorize n - 1 = 2^s * d, where d is odd.
- Implement the Miller-Rabin witness test.
- Test candidates using multiple bases (random CSPRNG bases or specified base list).
"""

import secrets
import random
import sys

# ==============================================================================
# Configuration & Assigned Parameters
# ==============================================================================
# Assigned bit length for cryptographic prime generation
BIT_LENGTH = 512

# Default security parameter: number of Miller-Rabin testing rounds
# 40 rounds gives an error probability <= 4^(-40) < 10^(-24)
DEFAULT_ROUNDS = 40


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


# ==============================================================================
# Commit 3: Miller–Rabin Primality Test
# ==============================================================================
def factorize_n_minus_1(n: int) -> tuple[int, int]:
    """
    Factorizes n - 1 into the form:
        n - 1 = 2^s * d
    where d is an odd integer and s >= 1.

    This decomposition extracts all factors of 2 from n - 1, which represents
    the cyclic structure used by the Miller-Rabin test.

    Args:
        n: An odd integer > 2.

    Returns:
        tuple[int, int]: (s, d) where n - 1 = (2^s) * d and d is odd.
    """
    if n <= 2 or n % 2 == 0:
        raise ValueError("Factorization requires an odd integer n > 2.")

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    return s, d


def is_witness(a: int, n: int, s: int, d: int) -> bool:
    """
    Determines whether a base 'a' is a Miller-Rabin witness to the
    compositeness of candidate 'n'.

    Witness Test Logic:
    1. Compute x = a^d mod n using fast modular exponentiation.
    2. If x == 1 or x == n - 1:
       'a' is not a witness (n passes this round). Return False.
    3. Repeat s - 1 times:
       x = (x * x) mod n
       If x == n - 1:
           'a' is not a witness (n passes this round). Return False.
       If x == 1:
           Non-trivial square root of 1 modulo n found; n is definitely composite.
           Return True.
    4. If the loop finishes without x == n - 1, Fermat's Little Theorem /
       Miller-Rabin condition is violated; n is composite. Return True.

    Args:
        a: Base integer in the range [2, n - 2].
        n: Odd candidate integer to test.
        s: Exponent of 2 in (n - 1 = 2^s * d).
        d: Odd component in (n - 1 = 2^s * d).

    Returns:
        bool: True if 'a' proves n is composite (witness found);
              False if n passes the test for base 'a' (probable prime for this base).
    """
    # Step 1: Compute x = a^d mod n
    x = modular_exponentiation(a, d, n)

    if x == 1 or x == n - 1:
        return False  # Not a witness; candidate passes

    # Step 2: Repeatedly square x up to s - 1 times
    for _ in range(s - 1):
        x = modular_exponentiation(x, 2, n)
        if x == n - 1:
            return False  # Candidate passes for this base
        if x == 1:
            return True   # Non-trivial square root of 1 mod n -> composite

    # Violated Miller-Rabin condition; 'a' is a witness to compositeness
    return True


def miller_rabin_test(n: int, rounds: int = DEFAULT_ROUNDS, bases: list[int] = None) -> bool:
    """
    Applies the Miller-Rabin probabilistic primality test to integer n.

    Tests the candidate across multiple bases to drive the error probability
    down to <= 4^(-k).

    Args:
        n: Integer candidate to test for primality.
        rounds: Number of testing rounds / random bases (default: 40).
        bases: Optional explicit list of bases to test against (e.g., [2, 3, 5, 7, ...]).
               If None, 'rounds' independent random bases in [2, n - 2] are chosen
               using CSPRNG.

    Returns:
        bool: True if n is a probable prime; False if n is definitely composite.
    """
    # Handle small integers and trivial cases
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Decompose n - 1 = 2^s * d
    s, d = factorize_n_minus_1(n)

    # If explicit bases are supplied, test candidate against them
    if bases is not None:
        for a in bases:
            a = a % n
            if a <= 1 or a == n - 1:
                continue
            if is_witness(a, n, s, d):
                return False  # Composite
        return True  # Passed all specified bases

    # Otherwise, perform 'rounds' tests using cryptographically secure random bases
    for _ in range(rounds):
        # Choose a uniform random base a in the range [2, n - 2]
        a = secrets.randbelow(n - 3) + 2
        if is_witness(a, n, s, d):
            return False  # Composite

    return True  # Probable prime


if __name__ == "__main__":
    print(f"[*] Assignment 8: Miller-Rabin Primality Test")
    print(f"[*] Assigned Bit Length: {BIT_LENGTH}")

    # Commit 1
    sample_candidate = generate_odd_candidate(BIT_LENGTH)
    print(f"\n--- [Commit 1] Candidate Generation ---")
    print(f"[*] Sample Candidate ({sample_candidate.bit_length()} bits):")
    print(f"    {sample_candidate}")
    print(f"[*] Validated (Odd & Exactly {BIT_LENGTH} bits): "
          f"{validate_candidate_properties(sample_candidate, BIT_LENGTH)}")

    # Commit 2
    print(f"\n--- [Commit 2] Fast Modular Exponentiation ---")
    test_base, test_exp = 2, 65537
    calc_res = modular_exponentiation(test_base, test_exp, sample_candidate)
    expected_res = pow(test_base, test_exp, sample_candidate)
    print(f"[*] Calculating ({test_base}^{test_exp}) mod candidate...")
    print(f"    Correctness check vs pow(): {calc_res == expected_res}")

    # Commit 3
    print(f"\n--- [Commit 3] Miller-Rabin Primality Test Verification ---")
    # Test known prime: Mersenne prime M31 = 2^31 - 1 = 2147483647
    m31 = (1 << 31) - 1
    s_m31, d_m31 = factorize_n_minus_1(m31)
    print(f"[*] Decomposition of M31 (2147483647): n-1 = 2^{s_m31} * {d_m31}")
    print(f"[*] M31 is probable prime: {miller_rabin_test(m31, rounds=20)}")

    # Test known composite / Carmichael number: 561 = 3 * 11 * 17
    carmichael_561 = 561
    print(f"[*] Carmichael number 561 is composite: {not miller_rabin_test(carmichael_561, bases=[2, 3])}")

    # Test Miller-Rabin on our random 512-bit candidate (expected composite almost certainly)
    print(f"[*] Random 512-bit candidate passes Miller-Rabin: {miller_rabin_test(sample_candidate, rounds=10)}")
