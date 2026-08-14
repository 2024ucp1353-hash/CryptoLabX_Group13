import os

BASE_RECORDS_DIR = os.path.join(os.path.dirname(__file__), "..", "records")


def download_medical_file_vulnerable():
    """Vulnerability 3: Path Traversal / Arbitrary File Access
    Fails to sanitize file path inputs. User input can contain '../' sequence
    allowing arbitrary file reading across the filesystem.
    Payload example: ../../README.md or ../../datasets/sample1.txt
    """
    print("\n========== DOWNLOAD MEDICAL FILE (VULNERABLE: Path Traversal) ==========")
    filename = input("Enter record file name to download: ").strip()

    # VULNERABILITY: Directly joining path without sanitizing filename with os.path.basename()
    target_path = os.path.join(BASE_RECORDS_DIR, filename)
    print(f"[DEBUG PATH]: {target_path}")

    try:
        if os.path.exists(target_path):
            with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            print("\n[FILE CONTENT RETRIEVED]:")
            print("-" * 40)
            print(content[:500])  # Print preview
            print("-" * 40)
        else:
            print(f"File '{filename}' not found at path: {target_path}")
    except Exception as e:
        print(f"Error accessing file: {e}")
