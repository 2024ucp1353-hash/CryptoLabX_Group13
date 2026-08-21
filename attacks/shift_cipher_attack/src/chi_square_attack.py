from shift_cipher import decrypt

english_frequency = {
    'a': 8.167,
    'b': 1.492,
    'c': 2.782,
    'd': 4.253,
    'e': 12.702,
    'f': 2.228,
    'g': 2.015,
    'h': 6.094,
    'i': 6.966,
    'j': 0.153,
    'k': 0.772,
    'l': 4.025,
    'm': 2.406,
    'n': 6.749,
    'o': 7.507,
    'p': 1.929,
    'q': 0.095,
    'r': 5.987,
    's': 6.327,
    't': 9.056,
    'u': 2.758,
    'v': 0.978,
    'w': 2.360,
    'x': 0.150,
    'y': 1.974,
    'z': 0.074
}


def chi_square_score(text):
    letters = [ch.lower() for ch in text if ch.isalpha()]
    total = len(letters)

    if total == 0:
        return float('inf')

    score = 0

    for letter in english_frequency:
        observed = letters.count(letter)
        expected = (english_frequency[letter] / 100) * total

        if expected > 0:
            score += ((observed - expected) ** 2) / expected

    return score


def chi_square_attack(ciphertext):
    best_key = 0
    best_plaintext = ""
    best_score = float('inf')

    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = chi_square_score(plaintext)

        if score < best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score


if __name__ == "__main__":
    ciphertext = input("Enter ciphertext: ")

    key, plaintext, score = chi_square_attack(ciphertext)

    print("Predicted Key:", key)
    print("Decrypted Text:", plaintext)
    print("Chi-Square Score:", round(score, 2))