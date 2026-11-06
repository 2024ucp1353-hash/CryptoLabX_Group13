import random
import secrets
import string
import time
from typing import Optional, Tuple, Dict

# ==============================================================================
# Configuration & Constants
# ==============================================================================
# Seed search space for 16-bit seeds (2^16 = 65,536)
SEED_16BIT_MAX = 65536

# Known target pattern of 14 consecutive 'A' characters
KNOWN_TARGET_PATTERN = b"A" * 14


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


# ==============================================================================
# Commit 2: MT19937 Stream Cipher (Encryption & Decryption)
# ==============================================================================
def mt19937_stream_cipher(data: bytes, seed: int) -> bytes:
    """
    MT19937 symmetric stream cipher engine.

    Generates one 8-bit keystream value per input byte using MT19937 and XORs
    it with the data. Because XOR is an involution (A ^ K ^ K = A), the exact
    same transformation performs both encryption and decryption when seeded
    identically.

    Args:
        data: Plaintext bytes (for encryption) or ciphertext bytes (for decryption).
        seed: Integer seed for MT19937 keystream generation.

    Returns:
        bytes: Transformed ciphertext or decrypted plaintext bytes.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")

    rng = init_mt19937(seed)
    return bytes(b ^ extract_keystream_byte(rng) for b in data)


def encrypt(plaintext: bytes, seed: int) -> bytes:
    """
    Encrypts plaintext bytes using the MT19937 stream cipher.

    Args:
        plaintext: Plaintext bytes to encrypt.
        seed: 16-bit or integer seed.

    Returns:
        bytes: Resulting ciphertext.
    """
    return mt19937_stream_cipher(plaintext, seed)


def decrypt(ciphertext: bytes, seed: int) -> bytes:
    """
    Decrypts ciphertext bytes using the MT19937 stream cipher.
    Re-uses the symmetric stream cipher function with the same seed.

    Args:
        ciphertext: Ciphertext bytes to decrypt.
        seed: Key/seed used during encryption.

    Returns:
        bytes: Decrypted plaintext.
    """
    return mt19937_stream_cipher(ciphertext, seed)


def verify_cipher_roundtrip(message: bytes, seed: int) -> bool:
    """
    Verifies that encryption followed by decryption recovers the exact original message.

    Args:
        message: Test message bytes.
        seed: Seed integer.

    Returns:
        bool: True if round-trip decryption matches original message.
    """
    ciphertext = encrypt(message, seed)
    recovered = decrypt(ciphertext, seed)
    return recovered == message


# ==============================================================================
# Commit 3: Plaintext Generation & Encryption
# ==============================================================================
def generate_16bit_seed() -> int:
    """
    Generates a cryptographically strong random 16-bit seed in [0, 65535].

    Returns:
        int: A 16-bit integer seed.
    """
    return secrets.randbelow(SEED_16BIT_MAX)


def generate_target_plaintext(
    min_prefix: int = 5,
    max_prefix: int = 20,
    known_pattern: bytes = KNOWN_TARGET_PATTERN
) -> Tuple[bytes, str]:
    """
    Generates a plaintext with a random 5–20 character printable prefix
    followed by 14 consecutive 'A' characters.

    Args:
        min_prefix: Minimum prefix length (default: 5).
        max_prefix: Maximum prefix length (default: 20).
        known_pattern: Target known pattern (default: 14 'A's).

    Returns:
        Tuple[bytes, str]: Complete plaintext as bytes and the generated prefix string.
    """
    prefix_length = secrets.randbelow(max_prefix - min_prefix + 1) + min_prefix
    alphabet = string.ascii_letters + string.digits
    prefix_str = "".join(secrets.choice(alphabet) for _ in range(prefix_length))
    plaintext = prefix_str.encode("utf-8") + known_pattern

    return plaintext, prefix_str


def create_encryption_challenge(
    seed: Optional[int] = None,
    min_prefix: int = 5,
    max_prefix: int = 20
) -> Dict[str, object]:
    """
    Generates a challenge consisting of random plaintext (prefix + 14 'A's),
    a random 16-bit seed, and the resulting MT19937 ciphertext.

    Args:
        seed: Optional specific 16-bit seed. If None, a random 16-bit seed is generated.
        min_prefix: Minimum prefix length (default: 5).
        max_prefix: Maximum prefix length (default: 20).

    Returns:
        Dict: Dictionary containing 'plaintext', 'prefix', 'seed', and 'ciphertext'.
    """
    if seed is None:
        seed = generate_16bit_seed()

    if not validate_16bit_seed(seed):
        raise ValueError(f"Seed {seed} is not a valid 16-bit integer.")

    plaintext, prefix_str = generate_target_plaintext(min_prefix, max_prefix)
    ciphertext = encrypt(plaintext, seed)

    return {
        "plaintext": plaintext,
        "prefix": prefix_str,
        "seed": seed,
        "ciphertext": ciphertext,
        "pattern": KNOWN_TARGET_PATTERN
    }


if __name__ == "__main__":
    print("[*] Assignment 10: MT19937 Stream Cipher & Predictable Token Attack")
    print(f"[*] 16-bit Seed Range: [0, {SEED_16BIT_MAX - 1}] (Total: {SEED_16BIT_MAX})")

    # Commit 1 Demo
    sample_seed = 12345
    print(f"\n--- [Commit 1] MT19937 Initialization & 8-bit Keystream ---")
    sample_keystream = generate_keystream(sample_seed, length=16)
    print(f"[*] Seed: {sample_seed}")
    print(f"[*] 16-byte keystream (hex): {sample_keystream.hex()}")
    print(f"[*] Seed validity check: {validate_16bit_seed(sample_seed)}")

    # Commit 2 Demo
    print(f"\n--- [Commit 2] Stream Cipher Encryption & Decryption ---")
    test_message = b"Cryptography Laboratory: Assignment 10 Stream Cipher Verification!"
    test_seed = 42424
    ciphertext = encrypt(test_message, test_seed)
    decrypted = decrypt(ciphertext, test_seed)
    print(f"[*] Test Plaintext        : {test_message}")
    print(f"[*] Ciphertext (hex)      : {ciphertext.hex()}")
    print(f"[*] Decrypted Plaintext   : {decrypted}")
    print(f"[*] Decryption matches original: {decrypted == test_message}")

    # Commit 3 Demo
    print(f"\n--- [Commit 3] Plaintext Generation & Encryption ---")
    challenge = create_encryption_challenge()
    print(f"[*] Generated Random 16-bit Seed : {challenge['seed']}")
    print(f"[*] Generated Prefix             : '{challenge['prefix']}' (len: {len(challenge['prefix'])})")
    print(f"[*] Complete Plaintext           : {challenge['plaintext']} (total len: {len(challenge['plaintext'])})")
    print(f"[*] Target Known Suffix          : {challenge['pattern']}")
    print(f"[*] Resulting Ciphertext (hex)   : {challenge['ciphertext'].hex()}")
