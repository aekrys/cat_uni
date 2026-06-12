import os

RECORD_FILE = "data/record.txt"


def load_record():
    try:
        with open(RECORD_FILE, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0


def save_record(score):
    os.makedirs("data", exist_ok=True)
    with open(RECORD_FILE, "w") as f:
        f.write(str(score))
