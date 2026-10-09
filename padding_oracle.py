
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16


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
    key = get_random_bytes(BLOCK_SIZE)
    iv = get_random_bytes(BLOCK_SIZE)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pkcs7_pad(plaintext.encode("utf-8"))
    ciphertext = cipher.encrypt(padded_text)

    return key, iv, ciphertext


def make_padding_oracle(key):
    # The key stays inside the oracle's private scope.
    def padding_oracle(ciphertext, iv):
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(ciphertext)
            pkcs7_unpad(decrypted)
            return True
        except (ValueError, TypeError):
            return False

    return padding_oracle


if __name__ == "__main__":
    message = "Hello, padding oracle!"
    key, iv, ciphertext = encrypt_message(message)

    # Create an oracle that keeps the key hidden from its caller.
    oracle = make_padding_oracle(key)

    print("Original plaintext:", message)
    print("IV:", iv.hex())
    print("Ciphertext:", ciphertext.hex())
    print("Ciphertext length:", len(ciphertext), "bytes")
    print("Original ciphertext has valid padding:",
          oracle(ciphertext, iv))