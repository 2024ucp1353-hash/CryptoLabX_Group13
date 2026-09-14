def clean_ciphertext(ciphertext):
    """
    Remove spaces and special characters from ciphertext
    and convert all letters to uppercase.
    """
    cleaned = ""

    for char in ciphertext:
        if char.isalpha():
            cleaned += char.upper()

    return cleaned


def main():
    with open("ciphertext/ciphertext.txt", "r") as file:
        ciphertext = file.read()

    ciphertext = clean_ciphertext(ciphertext)

    print("Cleaned Ciphertext:")
    print(ciphertext)
    print("\nCiphertext Length:", len(ciphertext))


if __name__ == "__main__":
    main()