
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16


# Commit 2: PKCS#7 padding and AES-CBC encryption
def pkcs7_pad(data):
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data):
    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Invalid padding")

    pad_len = data[-1]

    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding")

    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid padding")

    return data[:-pad_len]


def encrypt_message(plaintext):
    key = get_random_bytes(16)
    iv = get_random_bytes(BLOCK_SIZE)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pkcs7_pad(plaintext.encode("utf-8"))
    ciphertext = cipher.encrypt(padded_text)

    return key, iv, ciphertext


# Commit 3: Padding oracle
def make_padding_oracle(key):
    # The key remains inside the oracle's private scope.
    def padding_oracle(ciphertext, iv):
        try:
            if len(iv) != BLOCK_SIZE:
                return False

            if not ciphertext or len(ciphertext) % BLOCK_SIZE != 0:
                return False

            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(ciphertext)
            pkcs7_unpad(decrypted)
            return True

        except (ValueError, TypeError):
            return False

    return padding_oracle


# Commit 4: Ciphertext block preparation
def split_ciphertext(ciphertext):
    if not ciphertext or len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext must contain complete AES blocks")

    return [
        ciphertext[i:i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]


def prepare_attack_blocks(iv, ciphertext):
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV must be 16 bytes")

    # The IV precedes C1 and influences the first plaintext block.
    return [iv] + split_ciphertext(ciphertext)


def query_oracle(oracle, target_block, modified_previous_block):
    # The target block is decrypted using the supplied preceding block.
    return oracle(target_block, modified_previous_block)


# Commit 5: Byte-by-byte padding oracle attack
def attack_single_block(oracle, prev_block, target_block):
    """
    Recover the 16-byte plaintext block corresponding to target_block
    by modifying the preceding block (prev_block) and querying the padding oracle.
    Bytes are recovered from right to left (index 15 down to 0).
    """
    intermediate = bytearray(BLOCK_SIZE)
    plaintext_block = bytearray(BLOCK_SIZE)

    for byte_index in range(BLOCK_SIZE - 1, -1, -1):
        pad_val = BLOCK_SIZE - byte_index
        mod_prev = bytearray(prev_block)

        # Set already recovered bytes to produce the target pad_val
        for k in range(byte_index + 1, BLOCK_SIZE):
            mod_prev[k] = intermediate[k] ^ pad_val

        found = False
        for guess in range(256):
            mod_prev[byte_index] = guess
            if query_oracle(oracle, target_block, bytes(mod_prev)):
                # Disambiguate pad_val == 1 to avoid accidental multi-byte padding
                if pad_val == 1 and byte_index > 0:
                    check_prev = bytearray(mod_prev)
                    check_prev[byte_index - 1] ^= 1
                    if not query_oracle(oracle, target_block, bytes(check_prev)):
                        continue

                intermediate[byte_index] = guess ^ pad_val
                plaintext_block[byte_index] = intermediate[byte_index] ^ prev_block[byte_index]
                found = True
                break

        if not found:
            raise RuntimeError(f"Failed to recover byte at index {byte_index}")

    return bytes(plaintext_block)


# Local demonstration
if __name__ == "__main__":
    message = "Hello, padding oracle!"

    key, iv, ciphertext = encrypt_message(message)
    oracle = make_padding_oracle(key)

    blocks = prepare_attack_blocks(iv, ciphertext)

    print("Original plaintext:", message)
    print("IV:", iv.hex())
    print("Ciphertext:", ciphertext.hex())
    print("Number of ciphertext blocks:", len(blocks) - 1)

    for i, block in enumerate(blocks):
        label = "IV" if i == 0 else f"C{i}"
        print(f"{label}: {block.hex()}")

    print("\n--- Demonstrating Byte-by-Byte Attack on Block 1 ---")
    recovered_block1 = attack_single_block(oracle, blocks[0], blocks[1])
    print("Recovered Block 1 (raw bytes):", recovered_block1)
    print("Recovered Block 1 (ASCII):", recovered_block1.decode("latin1", errors="replace"))