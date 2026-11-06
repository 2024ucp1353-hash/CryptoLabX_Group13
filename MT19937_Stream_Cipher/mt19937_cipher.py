import random
import secrets
import string
import time
from typing import Optional

# ==============================================================================
# Configuration & Constants
# ==============================================================================
# Seed search space for 16-bit seeds (2^16 = 65,536)
SEED_16BIT_MAX = 65536


# ==============================================================================
# Commit 1: MT19937 Initialization & 8-bit Keystream Extraction
# ==============================================================================
def init_mt19937(seed: int) -> random.Random:
    """
    Initializes the Mersenne Twister MT19937 PRNG with a specific integer seed.

    Python's standard library `random` module uses MT19937 as its core generator.
    By instantiating `random.Random(seed)`, we maintain isolated, deterministic
    keystream generation.

    Args:
        seed: Integer seed used to initialize MT19937 state.

    Returns:
        random.Random: Initialized MT19937 PRNG instance.
    """
    return random.Random(seed)


def extract_keystream_byte(rng: random.Random) -> int:
    """
    Extracts one 8-bit keystream value (0-255) from the MT19937 generator.

    Args:
        rng: Initialized MT19937 instance.

    Returns:
        int: An 8-bit keystream value (0 <= byte <= 255).
    """
    return rng.getrandbits(8)


def generate_keystream(seed: int, length: int) -> bytes:
    """
    Generates an 8-bit keystream sequence of specified length from an MT19937 seed.

    Args:
        seed: Integer seed for MT19937 initialization.
        length: Number of consecutive 8-bit keystream bytes to generate.

    Returns:
        bytes: Generated keystream bytes.
    """
    if length < 0:
        raise ValueError("Keystream length cannot be negative.")
    rng = init_mt19937(seed)
    return bytes(extract_keystream_byte(rng) for _ in range(length))


def validate_16bit_seed(seed: int) -> bool:
    """
    Validates whether an integer seed falls within the valid 16-bit range [0, 65535].

    Args:
        seed: Seed to validate.

    Returns:
        bool: True if seed is within [0, 65535], False otherwise.
    """
    return isinstance(seed, int) and 0 <= seed < SEED_16BIT_MAX


if __name__ == "__main__":
    print("[*] Assignment 10: MT19937 Stream Cipher & Predictable Token Attack")
    print(f"[*] 16-bit Seed Range: [0, {SEED_16BIT_MAX - 1}] (Total: {SEED_16BIT_MAX})")

    # Sample MT19937 initialization & keystream extraction demo
    sample_seed = 12345
    print(f"[*] Testing MT19937 initialization with seed = {sample_seed}...")
    sample_keystream = generate_keystream(sample_seed, length=16)
    print(f"    Extracted 16-byte keystream (hex): {sample_keystream.hex()}")
    print(f"    Seed validity check: {validate_16bit_seed(sample_seed)}")
