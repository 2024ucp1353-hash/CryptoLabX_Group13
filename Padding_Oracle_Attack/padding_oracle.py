
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


# Commit 6: Complete plaintext recovery across all blocks
def recover_plaintext(oracle, iv, ciphertext):
    """
    Recover the complete plaintext from an AES-CBC ciphertext using the padding oracle.
    Iterates across all ciphertext blocks, reconstructs the full plaintext,
    and removes PKCS#7 padding.
    """
    blocks = prepare_attack_blocks(iv, ciphertext)
    recovered_bytes = bytearray()

    for i in range(1, len(blocks)):
        prev_block = blocks[i - 1]
        target_block = blocks[i]
        block_plaintext = attack_single_block(oracle, prev_block, target_block)
        recovered_bytes.extend(block_plaintext)

    unpadded_bytes = pkcs7_unpad(bytes(recovered_bytes))
    return unpadded_bytes.decode("utf-8")


# Commit 7: Track oracle queries and analyze attack results
class OracleQueryTracker:
    """
    Wraps a padding oracle function to track the total number of queries
    submitted during the cryptanalysis.
    """
    def __init__(self, oracle):
        self._oracle = oracle
        self.query_count = 0

    def __call__(self, ciphertext, iv):
        self.query_count += 1
        return self._oracle(ciphertext, iv)

    def reset(self):
        self.query_count = 0


def attack_and_analyze(oracle, iv, ciphertext, verbose=True):
    """
    Executes the padding oracle attack while instrumenting and recording
    oracle queries per block and overall. Displays detailed metrics and analysis.
    """
    tracker = OracleQueryTracker(oracle)
    blocks = prepare_attack_blocks(iv, ciphertext)
    num_ciphertext_blocks = len(blocks) - 1

    if verbose:
        print("==================================================")
        print("    PADDING ORACLE ATTACK EXECUTION & ANALYSIS   ")
        print("==================================================")
        print(f"Total Ciphertext Length : {len(ciphertext)} bytes")
        print(f"Total Ciphertext Blocks : {num_ciphertext_blocks} (16 bytes each)")
        print(f"IV (Hex)                : {iv.hex()}\n")

    recovered_raw_blocks = []
    block_queries = []

    for i in range(1, len(blocks)):
        prev_block = blocks[i - 1]
        target_block = blocks[i]
        queries_before = tracker.query_count

        recovered_blk = attack_single_block(tracker, prev_block, target_block)
        queries_for_block = tracker.query_count - queries_before

        recovered_raw_blocks.append(recovered_blk)
        block_queries.append(queries_for_block)

        if verbose:
            avg_per_byte = queries_for_block / BLOCK_SIZE
            blk_ascii = recovered_blk.decode("latin1", errors="replace")
            print(f"[*] Recovered Block {i}/{num_ciphertext_blocks}:")
            print(f"    Raw Hex        : {recovered_blk.hex()}")
            print(f"    Text Preview   : {repr(blk_ascii)}")
            print(f"    Block Queries  : {queries_for_block} (avg {avg_per_byte:.1f} queries/byte)\n")

    full_padded_bytes = b"".join(recovered_raw_blocks)
    unpadded_bytes = pkcs7_unpad(full_padded_bytes)
    plaintext = unpadded_bytes.decode("utf-8")

    total_queries = tracker.query_count
    total_bytes = num_ciphertext_blocks * BLOCK_SIZE
    overall_avg = total_queries / total_bytes

    if verbose:
        print("==================================================")
        print("                 ATTACK SUMMARY                   ")
        print("==================================================")
        print(f"Recovered Plaintext     : {plaintext}")
        print(f"Total Blocks Recovered  : {num_ciphertext_blocks}")
        print(f"Total Plaintext Bytes   : {len(unpadded_bytes)} (padded: {total_bytes})")
        print(f"Total Oracle Queries    : {total_queries}")
        print(f"Average Queries / Byte  : {overall_avg:.2f} (Theoretical expected: ~128)")
        print(f"Max Possible Queries    : {total_bytes * 256} ({total_bytes} x 256)")
        print(f"Brute Force Key Space   : 2^128 (~3.4 x 10^38)")
        print("==================================================\n")

    return {
        "plaintext": plaintext,
        "total_queries": total_queries,
        "block_queries": block_queries,
        "average_queries_per_byte": overall_avg,
    }


# Local demonstration
if __name__ == "__main__":
    message = "Cryptography Lab 7: Padding Oracle Attack demonstration on AES-CBC!"

    key, iv, ciphertext = encrypt_message(message)
    oracle = make_padding_oracle(key)

    results = attack_and_analyze(oracle, iv, ciphertext, verbose=True)

    print("Verification check against original plaintext:",
          results["plaintext"] == message)