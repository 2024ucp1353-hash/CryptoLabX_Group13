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


# ==============================================================================
# Commit 4: Candidate Generation Loop
# ==============================================================================
def candidate_generation_loop(
    bit_length: int = BIT_LENGTH,
    rounds: int = DEFAULT_ROUNDS,
    on_candidate_tested=None
) -> int:
    """
    Candidate Generation Loop:
    Repeatedly generates random odd candidates of the assigned bit length,
    applies the Miller-Rabin primality test, rejects composite candidates,
    and repeats until a probable prime candidate is found.

    Args:
        bit_length: Assigned bit length of the candidate (default: 512).
        rounds: Number of Miller-Rabin testing rounds per candidate (default: 40).
        on_candidate_tested: Optional callback hook invoked as
                             on_candidate_tested(candidate, is_probable_prime)
                             after each candidate is tested. Useful for tracking
                             metrics in subsequent steps.

    Returns:
        int: A probable prime integer of exactly `bit_length` bits that passed
             all Miller-Rabin testing rounds.
    """
    while True:
        # Step 1: Generate random odd candidate
        candidate = generate_odd_candidate(bit_length)

        # Step 2: Apply the Miller-Rabin primality test
        is_probable_prime = miller_rabin_test(candidate, rounds=rounds)

        # Optional hook for metrics tracking
        if on_candidate_tested is not None:
            on_candidate_tested(candidate, is_probable_prime)

        # Step 3: Reject composite candidates and repeat until a probable prime is found
        if is_probable_prime:
            return candidate


if __name__ == "__main__":

    print("\n===== 512-BIT MILLER-RABIN PRIME GENERATION =====")

    candidate_count = 0

    def count_candidate(candidate, is_probable_prime):
        global candidate_count
        candidate_count += 1

    print("\nGenerating probable prime...")

    found_prime = candidate_generation_loop(
        bit_length=BIT_LENGTH,
        rounds=DEFAULT_ROUNDS,
        on_candidate_tested=count_candidate
    )

    print("\nPrime generation completed!")
    print("Generated prime:", found_prime)
    print("Bit length:", found_prime.bit_length())
    print("Candidates tested:", candidate_count)
    print("Miller-Rabin rounds:", DEFAULT_ROUNDS)