import os
import hashlib


def generate_id(file_path: str) -> str:
    h = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)

    return h.hexdigest()


def get_file_type(file_path: str) -> str:
    _, ext = os.path.splitext(file_path)
    return ext.replace(".", "") if ext else "unknown"