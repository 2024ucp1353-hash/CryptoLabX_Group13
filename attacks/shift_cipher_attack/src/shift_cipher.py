"""
Shift Cipher (Caesar Cipher) Implementation
CryptoLab - Group 13
"""

def encrypt(plaintext: str, key: int) -> str:
    """
    Encrypts plaintext using the Shift (Caesar) Cipher with the given key.
    Preserves uppercase and lowercase letters; non-alphabetic characters remain unchanged.
    
    :param plaintext: The string message to encrypt
    :param key: Shift amount (0-25, supports any integer modulo 26)
    :return: The encrypted ciphertext
    """
    shift = key % 26
    ciphertext = []
    
    for char in plaintext:
        if char.isupper():
            shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            ciphertext.append(shifted)
        elif char.islower():
            shifted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            ciphertext.append(shifted)
        else:
            ciphertext.append(char)
            
    return "".join(ciphertext)


def decrypt(ciphertext: str, key: int) -> str:
    """
    Decrypts ciphertext using the Shift (Caesar) Cipher with the given key.
    
    :param ciphertext: The encrypted message string
    :param key: Shift amount used during encryption
    :return: The decrypted plaintext
    """
    return encrypt(ciphertext, -key)


if __name__ == "__main__":
    print("=== Shift Cipher Module Test ===")
    sample_text = "The quick brown fox jumps over the lazy dog!"
    test_key = 3
    encrypted = encrypt(sample_text, test_key)
    decrypted = decrypt(encrypted, test_key)
    
    print(f"Original Text : {sample_text}")
    print(f"Key           : {test_key}")
    print(f"Encrypted     : {encrypted}")
    print(f"Decrypted     : {decrypted}")
    assert decrypted == sample_text, "Decryption failed!"
    print("Verification Passed: Decrypted text matches the original plaintext.")
