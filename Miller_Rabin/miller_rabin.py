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


if __name__ == "__main__":
    print(f"[*] Assignment 8: Miller-Rabin Primality Test")
    print(f"[*] Assigned Bit Length: {BIT_LENGTH}")
    
    # Generate and test a sample candidate
    sample_candidate = generate_odd_candidate(BIT_LENGTH)
    print(f"[*] Sample Candidate Generated ({sample_candidate.bit_length()} bits):")
    print(f"    {sample_candidate}")
    print(f"[*] Validation Check (Odd & Exactly {BIT_LENGTH} bits): "
          f"{validate_candidate_properties(sample_candidate, BIT_LENGTH)}")
