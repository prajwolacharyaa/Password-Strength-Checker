import re


KEYBOARD_PATTERNS = (
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "123456",
    "654321",
)


def detect_patterns(password: str) -> list[str]:
    lowered = password.lower()
    findings: list[str] = []

    if re.search(r"(.)\1{2,}", password):
        findings.append("Contains repeated characters.")

    if re.search(r"(0123|1234|2345|3456|4567|5678|6789)", lowered):
        findings.append("Contains sequential numbers.")

    if re.search(r"(abcd|bcde|cdef|defg|wxyz)", lowered):
        findings.append("Contains sequential letters.")

    if any(pattern in lowered for pattern in KEYBOARD_PATTERNS):
        findings.append("Contains a common keyboard pattern.")

    return findings
