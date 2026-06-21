import os

RECORD_FILE = "data/record.txt"


def load_record():
    """
    Загружает рекорд из файла
    Если файла нет, рекорд 0
    """

    try:
        with open(RECORD_FILE, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0


def save_record(score):
    """
    Сохраняет рекорд в файл
    """

    os.makedirs("data", exist_ok=True)
    with open(RECORD_FILE, "w") as f:
        f.write(str(score))
