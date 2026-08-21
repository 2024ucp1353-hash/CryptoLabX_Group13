"""
Brute Force and Dictionary Scoring Attack
CryptoLab - Group 13
"""

from shift_cipher import decrypt


def load_dictionary(filename: str) -> set:
    """
    Loads English words from a dictionary file.

    :param filename: Path to dictionary file
    :return: Set containing English words
    """
    words = set()

    with open(filename, "r") as file:
        for line in file:
            word = line.strip().lower()

            if word:
                words.add(word)

    return words


def dictionary_score(text: str, dictionary: set) -> int:
    """
    Calculates the dictionary score of a plaintext.

    The score is the number of words in the plaintext
    that are present in the English dictionary.

    :param text: Plaintext to score
    :param dictionary: Set of English words
    :return: Dictionary score
    """
    words = text.lower().split()
    score = 0

    for word in words:
        word = "".join(
            char for char in word
            if char.isalpha()
        )

        if word in dictionary:
            score += 1

    return score


def brute_force_attack(ciphertext: str, dictionary: set):
    """
    Tries all possible Shift Cipher keys from 0 to 25.

    Each decrypted plaintext is scored using the English
    dictionary. The plaintext with the highest score
    is selected as the most likely plaintext.

    :param ciphertext: Encrypted text
    :param dictionary: Set of English words
    :return: Predicted key, plaintext and dictionary score
    """

    best_key = 0
    best_plaintext = ""
    best_score = -1

    print("\n=== Brute Force Dictionary Attack ===")

    for key in range(26):
        plaintext = decrypt(ciphertext, key)

        score = dictionary_score(
            plaintext,
            dictionary
        )

        print(
            f"Key: {key:2} | "
            f"Score: {score:2} | "
            f"{plaintext}"
        )

        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score


if __name__ == "__main__":

    print("=== Shift Cipher Brute Force Attack ===")

    ciphertext = input("Enter ciphertext: ")

    dictionary_file = "dictionary/english_words.txt"

    dictionary = load_dictionary(dictionary_file)

    key, plaintext, score = brute_force_attack(
        ciphertext,
        dictionary
    )

    print("\n=== Result ===")
    print("Predicted Key   :", key)
    print("Plaintext       :", plaintext)
    print("Dictionary Score:", score)