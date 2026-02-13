import os

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def count_lines(file_path):
    try:
        with open(file_path, "r") as f:
            return sum(1 for _ in f)
    except:
        return 0
