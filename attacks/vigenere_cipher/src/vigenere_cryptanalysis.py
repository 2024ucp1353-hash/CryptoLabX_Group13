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


def find_repeated_patterns(ciphertext, min_length=3, max_length=5):
    """
    Find repeated sequences of letters in the ciphertext.

    Returns:
        A dictionary where each repeated pattern is mapped
        to the positions where it occurs.
    """

    patterns = {}

    for length in range(min_length, max_length + 1):

        for i in range(len(ciphertext) - length + 1):

            pattern = ciphertext[i:i + length]

            if pattern not in patterns:
                patterns[pattern] = []

            patterns[pattern].append(i)

    repeated_patterns = {}

    for pattern, positions in patterns.items():

        if len(positions) > 1:
            repeated_patterns[pattern] = positions

    return repeated_patterns


def calculate_distances(repeated_patterns):
    """
    Calculate distances between repeated occurrences
    of each pattern.
    """

    distances = {}

    for pattern, positions in repeated_patterns.items():

        pattern_distances = []

        for i in range(len(positions)):

            for j in range(i + 1, len(positions)):

                distance = positions[j] - positions[i]

                pattern_distances.append(distance)

        distances[pattern] = pattern_distances

    return distances


def main():
    # Read ciphertext from file
    with open("ciphertext/ciphertext.txt", "r") as file:
        ciphertext = file.read()

    # Preprocess ciphertext
    ciphertext = clean_ciphertext(ciphertext)

    print("======================================")
    print("VIGENERE CIPHER CRYPTANALYSIS")
    print("======================================")

    print("\nCiphertext Length:", len(ciphertext))

    # Find repeated patterns
    repeated_patterns = find_repeated_patterns(ciphertext)

    print("\nRepeated Patterns:")
    print("--------------------------------------")

    for pattern, positions in repeated_patterns.items():
        print(pattern, "->", positions)

    # Calculate distances
    distances = calculate_distances(repeated_patterns)

    print("\nDistances Between Repeated Patterns:")
    print("--------------------------------------")

    for pattern, pattern_distances in distances.items():
        print(pattern, "->", pattern_distances)


if __name__ == "__main__":
    main()