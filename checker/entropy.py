import math
import re


def _pool_size(password: str) -> int:
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[^A-Za-z0-9]", password):
        pool += 32
    return pool


def calculate_entropy(password: str) -> float:
    if not password:
        return 0.0

    pool = _pool_size(password)
    if pool == 0:
        return 0.0

    return round(len(password) * math.log2(pool), 2)
