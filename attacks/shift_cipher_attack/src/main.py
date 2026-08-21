import os

from shift_cipher import encrypt, decrypt
from brute_force_dictionary import load_dictionary, brute_force_attack
from chi_square_attack import chi_square_attack


def main():
    print("==========================================")
    print("       SHIFT CIPHER CRYPTANALYSIS")
    print("              CryptoLabX")
    print("==========================================")

    plaintext = input("\nEnter plaintext: ")
    key = int(input("Enter key (0-25): "))

    ciphertext = encrypt(plaintext, key)

    print("\n=== Encryption ===")
    print("Plaintext  :", plaintext)
    print("Key        :", key)
    print("Ciphertext :", ciphertext)

    decrypted = decrypt(ciphertext, key)

    print("\n=== Decryption ===")
    print("Key        :", key)
    print("Plaintext  :", decrypted)

    dictionary_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "dictionary",
        "english_words.txt"
    )


    if os.path.exists(dictionary_path):
        dictionary = load_dictionary(dictionary_path)

        brute_key, brute_plaintext, brute_score = brute_force_attack(
            ciphertext,
            dictionary
        )

        print("\n=== Brute Force Result ===")
        print("Predicted Key     :", brute_key)
        print("Plaintext         :", brute_plaintext)
        print("Dictionary Score  :", brute_score)
    else:
        print("Dictionary file not found.")
        brute_key = "N/A"
        brute_plaintext = "N/A"
        brute_score = "N/A"

    print("\n=== Chi-Square Attack ===")

    chi_key, chi_plaintext, chi_score = chi_square_attack(ciphertext)

    print("\n=== Chi-Square Result ===")
    print("Predicted Key     :", chi_key)
    print("Plaintext         :", chi_plaintext)
    print("Chi-Square Score  :", round(chi_score, 2))

    print("\n==========================================")
    print("              FINAL RESULTS")
    print("==========================================")
    print("Original Key      :", key)
    print("Brute Force Key   :", brute_key)
    print("Chi-Square Key    :", chi_key)
    print("Original Plaintext:", plaintext)
    print("Brute Force Text  :", brute_plaintext)
    print("Chi-Square Text   :", chi_plaintext)
    print("==========================================")


if __name__ == "__main__":
    main()