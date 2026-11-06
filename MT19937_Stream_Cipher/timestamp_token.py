
import random
import time


# Commit 5: Timestamp-Based Token Generation

TOKEN_LENGTH = 16


def generate_timestamp_token():
    # Record current Unix timestamp
    timestamp = int(time.time())

    # Initialize MT19937 using timestamp as seed
    rng = random.Random(timestamp)

    # Generate 16 consecutive 8-bit outputs
    token_bytes = bytes(rng.getrandbits(8) for _ in range(TOKEN_LENGTH))

    return timestamp, token_bytes


if __name__ == "__main__":

    print("=" * 55)
    print("       TIMESTAMP-BASED TOKEN GENERATION")
    print("=" * 55)

    timestamp, token = generate_timestamp_token()

    print("\nCurrent Unix Timestamp:", timestamp)
    print("Generated Token (Hex):", token.hex())
    print("Token Length:", len(token), "bytes")
    print("Token Generation Successful!")
