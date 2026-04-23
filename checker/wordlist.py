from pathlib import Path


WORDLIST_PATH = Path(__file__).resolve().parent.parent / "data" / "common_passwords.txt"


def load_common_passwords() -> set[str]:
    if not WORDLIST_PATH.exists():
        return set()

    return {
        line.strip().lower()
        for line in WORDLIST_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
