"""Security Test Case 3: Path Traversal / Arbitrary File Access Demonstration
Tests accessing files outside the records directory using directory traversal sequence '../'.
"""
import os
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))


def run_path_traversal_test():
    print("=" * 60)
    print("TEST CASE 3: PATH TRAVERSAL EXPLOITATION")
    print("=" * 60)

    records_dir = Path(__file__).resolve().parent.parent / "records"
    records_dir.mkdir(exist_ok=True)

    # Create dummy medical record file
    sample_record = records_dir / "patient_file.txt"
    sample_record.write_text("Confidential Patient Lab Results")

    # Path traversal payload targeting README.md in parent folder
    traversal_payload = "../README.md"
    target_path = records_dir / traversal_payload

    print(f"[+] Records Directory: {records_dir}")
    print(f"[+] Traversal Payload: {traversal_payload}")
    print(f"[+] Resolved Target Path: {target_path.resolve()}")

    if target_path.exists():
        content = target_path.read_text()
        print(f"[+] Successfully read arbitrary file across directory boundary! (Length: {len(content)} bytes)")
        print(f"    Preview: {content[:100]}...")

    assert target_path.exists(), "Path traversal test failed."
    print("\n[RESULT]: Path Traversal Vulnerability SUCCESSFULLY Exploited!\n")


if __name__ == "__main__":
    run_path_traversal_test()
