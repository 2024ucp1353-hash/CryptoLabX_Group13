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


def find_factors(distance):
    """
    Find all factors of a given distance.

    Factors from 2 onwards are considered because
    a key length of 1 is not useful for Kasiski analysis.
    """

    factors = []

    for i in range(2, distance + 1):

        if distance % i == 0:
            factors.append(i)

    return factors


def kasiski_analysis(distances, max_key_length=20):
    """
    Perform Kasiski examination.

    Counts how frequently each possible key length
    occurs as a factor of the distances between
    repeated patterns.

    Returns:
        A list of (key_length, count) sorted by
        frequency in descending order.
    """

    factor_count = {}

    for pattern, pattern_distances in distances.items():

        for distance in pattern_distances:

            factors = find_factors(distance)

            for factor in factors:

                if factor <= max_key_length:

                    if factor not in factor_count:
                        factor_count[factor] = 0

                    factor_count[factor] += 1

    candidates = sorted(
        factor_count.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return candidates


def calculate_ic(text):
    """
    Calculate the Index of Coincidence (IC) of a text.

    IC = sum(f_i * (f_i - 1)) / (N * (N - 1))

    where:
        f_i = frequency of each letter
        N   = total number of letters
    """

    n = len(text)

    if n <= 1:
        return 0.0

    frequencies = [0] * 26

    for char in text:

        if 'A' <= char <= 'Z':

            index = ord(char) - ord('A')

            frequencies[index] += 1

    numerator = 0

    for frequency in frequencies:

        numerator += frequency * (frequency - 1)

    denominator = n * (n - 1)

    return numerator / denominator


def split_into_groups(ciphertext, key_length):
    """
    Divide the ciphertext into groups according to
    the candidate key length.

    Each group contains characters encrypted using
    the same key position.
    """

    groups = []

    for i in range(key_length):

        group = ciphertext[i::key_length]

        groups.append(group)

    return groups


def calculate_average_ic(ciphertext, key_length):
    """
    Calculate the average Index of Coincidence
    across all groups for a given key length.
    """

    groups = split_into_groups(ciphertext, key_length)

    total_ic = 0

    for group in groups:

        total_ic += calculate_ic(group)

    return total_ic / len(groups)


def find_best_key_length(ciphertext, candidates):
    """
    Use Index of Coincidence to select the strongest
    key length from the Kasiski candidates.

    The candidate with the highest average IC is selected.
    """

    best_key_length = None
    best_ic = 0

    for key_length, count in candidates:

        average_ic = calculate_average_ic(
            ciphertext,
            key_length
        )

        if average_ic > best_ic:

            best_ic = average_ic
            best_key_length = key_length

    return best_key_length, best_ic


ENGLISH_LETTER_FREQUENCIES = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]


def frequency_analysis(group):
    """
    Calculate the letter frequency distribution (A-Z) for a ciphertext group.

    Returns:
        A tuple of (counts, percentages, most_frequent) where:
        - counts: dictionary of letter -> count
        - percentages: dictionary of letter -> percentage
        - most_frequent: list of most frequent letter(s)
    """
    n = len(group)
    counts = {chr(ord('A') + i): 0 for i in range(26)}

    for char in group:
        if 'A' <= char <= 'Z':
            counts[char] += 1

    percentages = {}
    for letter, count in counts.items():
        percentages[letter] = (count * 100.0 / n) if n > 0 else 0.0

    max_count = max(counts.values()) if counts else 0
    most_frequent = [letter for letter, count in counts.items() if count == max_count and max_count > 0]

    return counts, percentages, most_frequent


def find_shift(group):
    """
    Estimate the Caesar shift for a single ciphertext group
    using Chi-Square goodness-of-fit against standard English letter frequencies.

    Returns:
        The shift amount (0-25) corresponding to the key letter.
    """
    n = len(group)
    if n == 0:
        return 0

    best_shift = 0
    best_chi_square = float('inf')

    for shift in range(26):
        chi_square = 0.0
        decrypted = [chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in group]

        for i in range(26):
            target_letter = chr(ord('A') + i)
            observed = decrypted.count(target_letter)
            expected = ENGLISH_LETTER_FREQUENCIES[i] * n

            if expected > 0:
                chi_square += ((observed - expected) ** 2) / expected

        if chi_square < best_chi_square:
            best_chi_square = chi_square
            best_shift = shift

    return best_shift


def find_key(groups):
    """
    Determine the probable Vigenère key by combining the Caesar shifts
    discovered for each ciphertext group.

    Returns:
        The recovered key string.
    """
    key_chars = []

    for group in groups:
        shift = find_shift(group)
        key_char = chr(ord('A') + shift)
        key_chars.append(key_char)

    return "".join(key_chars)


def vigenere_decrypt(ciphertext, key):
    """
    Decrypt the ciphertext using the Vigenère cipher key.

    Returns:
        The decrypted plaintext string.
    """
    plaintext = []
    key_length = len(key)

    for i, char in enumerate(ciphertext):
        if 'A' <= char <= 'Z':
            shift = ord(key[i % key_length].upper()) - ord('A')
            plain_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            plaintext.append(plain_char)
        else:
            plaintext.append(char)

    return "".join(plaintext)


def vigenere_encrypt(plaintext, key):
    """
    Encrypt the plaintext using the Vigenère cipher key.

    Returns:
        The encrypted ciphertext string.
    """
    ciphertext = []
    key_length = len(key)

    for i, char in enumerate(plaintext):
        if 'A' <= char <= 'Z':
            shift = ord(key[i % key_length].upper()) - ord('A')
            cipher_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            ciphertext.append(cipher_char)
        else:
            ciphertext.append(char)

    return "".join(ciphertext)


def verify(ciphertext, plaintext, key):
    """
    Verify the cryptanalysis solution by re-encrypting the recovered plaintext
    and checking if it exactly matches the original ciphertext.

    Returns:
        Boolean indicating verification success.
    """
    re_encrypted = vigenere_encrypt(plaintext, key)
    is_match = (re_encrypted == ciphertext)

    print("\n======================================")
    print("SOLUTION VERIFICATION")
    print("======================================")
    print("1. Original Ciphertext Length :", len(ciphertext))
    print("2. Re-encrypted Length        :", len(re_encrypted))
    print("3. Exact Character Match      :", is_match)

    if is_match:
        print("4. Verification Status        : [PASSED - 100% Correct Recovery]")
    else:
        print("4. Verification Status        : [FAILED - Mismatch Detected]")

    print("======================================")
    return is_match


def main():
    # --------------------------------------
    # READ AND CLEAN CIPHERTEXT
    # --------------------------------------

    with open("ciphertext/ciphertext.txt", "r") as file:
        ciphertext = file.read()

    ciphertext = clean_ciphertext(ciphertext)

    print("======================================")
    print("VIGENERE CIPHER CRYPTANALYSIS")
    print("======================================")

    print("\nCiphertext Length:", len(ciphertext))

    # --------------------------------------
    # KASISKI ANALYSIS
    # --------------------------------------

    repeated_patterns = find_repeated_patterns(ciphertext)
    distances = calculate_distances(repeated_patterns)

    candidates = kasiski_analysis(distances)

    print("\nKasiski Key Length Candidates:")
    print("--------------------------------------")

    for key_length, count in candidates:

        print(
            "Key Length:",
            key_length,
            "| Factor Count:",
            count
        )

    # --------------------------------------
    # INDEX OF COINCIDENCE ANALYSIS
    # --------------------------------------

    print("\nIndex of Coincidence Analysis:")
    print("--------------------------------------")

    print("Key Length | Average IC")
    print("--------------------------------------")

    for key_length in range(1, 21):

        average_ic = calculate_average_ic(
            ciphertext,
            key_length
        )

        print(
            f"{key_length:10} | {average_ic:.4f}"
        )

    # --------------------------------------
    # SELECT BEST KEY LENGTH
    # --------------------------------------

    best_key_length, best_ic = find_best_key_length(
        ciphertext,
        candidates
    )

    print("\nEstimated Key Length:")
    print("--------------------------------------")

    print(
        "Key Length:",
        best_key_length
    )

    print(
        "Average IC:",
        round(best_ic, 4)
    )

    # --------------------------------------
    # SPLIT CIPHERTEXT INTO GROUPS
    # --------------------------------------

    groups = split_into_groups(
        ciphertext,
        best_key_length
    )

    print(
        "\nCiphertext Groups for Key Length",
        best_key_length
    )

    print("--------------------------------------")

    for i, group in enumerate(groups):

        print(
            "Group",
            i + 1,
            ":",
            group
        )

        print(
            "IC:",
            round(calculate_ic(group), 4)
        )

    # --------------------------------------
    # GROUP FREQUENCY ANALYSIS
    # --------------------------------------

    print("\n======================================")
    print("GROUP FREQUENCY ANALYSIS & SHIFTS")
    print("======================================")

    for i, group in enumerate(groups):
        counts, percentages, most_frequent = frequency_analysis(group)
        shift = find_shift(group)
        key_char = chr(ord('A') + shift)
        top_letters = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:4]
        top_str = ", ".join([f"{l}: {c}" for l, c in top_letters if c > 0])
        print(f"Group {i + 1:2} | Length: {len(group):2} | Top: {top_str:20} | Estimated Shift: {shift:2} -> Key Letter: '{key_char}'")

    # --------------------------------------
    # RECOVER VIGENERE KEY
    # --------------------------------------

    recovered_key = find_key(groups)

    print("\n======================================")
    print("RECOVERED VIGENERE KEY")
    print("======================================")
    print("Probable Key:", recovered_key)

    # --------------------------------------
    # DECRYPT CIPHERTEXT
    # --------------------------------------

    recovered_plaintext = vigenere_decrypt(ciphertext, recovered_key)

    print("\n======================================")
    print("RECOVERED PLAINTEXT")
    print("======================================")
    print("Plaintext Length:", len(recovered_plaintext))
    print("\nPlaintext Content:\n")
    print(recovered_plaintext)

    # --------------------------------------
    # VERIFY SOLUTION
    # --------------------------------------

    verify(ciphertext, recovered_plaintext, recovered_key)


if __name__ == "__main__":
    main()