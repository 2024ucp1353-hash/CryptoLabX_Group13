from collections import Counter
import os


def analyze_file():

    filename = input("\nEnter the filename (inside datasets folder): ").strip()

    filepath = os.path.join("datasets", filename)

    if not os.path.exists(filepath):
        print("\nError: File not found!")
        return

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()

        characters = len(text)
        words = len(text.split())
        lines = len(text.splitlines())
        unique_characters = len(set(text))

        letters = [ch.lower() for ch in text if ch.isalpha()]
        frequency = Counter(letters)

        print("\n========== File Analysis ==========")
        print(f"Characters       : {characters}")
        print(f"Words            : {words}")
        print(f"Lines            : {lines}")
        print(f"Unique Characters: {unique_characters}")

        print("\nLetter Frequency")
        print("-" * 25)

        for letter in sorted(frequency):
            print(f"{letter} : {frequency[letter]}")

    except Exception as e:
        print(f"\nError: {e}")