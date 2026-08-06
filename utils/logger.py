import os
from datetime import datetime

LOG_DIR = "outputs"
LOG_FILE = os.path.join(LOG_DIR, "execution.log")


def log_execution(option_name: str) -> None:
    """Logs the date, time, and selected menu option to execution.log."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] - Selected Option: {option_name}\n"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Logging error: {e}")
