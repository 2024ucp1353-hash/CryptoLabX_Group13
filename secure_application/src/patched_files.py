import os
from pathlib import Path

BASE_RECORDS_DIR = Path(__file__).resolve().parent.parent / "records"


def download_medical_file_secure():
    """FIX 3: Path Traversal Remediation
    Sanitizes filenames using os.path.basename() and enforces absolute path boundaries
    to prevent directory traversal attacks (e.g. '../').
    """
    print("\n========== DOWNLOAD MEDICAL FILE (SECURE: Boundary Checked) ==========")
    filename = input("Enter record file name to download: ").strip()

    # SECURE: Strip directory components using os.path.basename
    safe_filename = os.path.basename(filename)
    target_path = (BASE_RECORDS_DIR / safe_filename).resolve()

    # Verify target path remains within BASE_RECORDS_DIR boundary
    try:
        target_path.relative_to(BASE_RECORDS_DIR.resolve())
    except ValueError:
        print("\n[SECURITY ERROR]: Path Traversal Attempt Detected! Access Denied.")
        return

    if target_path.exists() and target_path.is_file():
        with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        print("\n[FILE CONTENT RETRIEVED SECURELY]:")
        print("-" * 40)
        print(content[:500])
        print("-" * 40)
    else:
        print(f"File '{safe_filename}' not found.")
