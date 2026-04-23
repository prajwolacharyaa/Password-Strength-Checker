import re

from checker.entropy import calculate_entropy
from checker.patterns import detect_patterns
from checker.wordlist import load_common_passwords

COMMON_PASSWORDS = load_common_passwords()


def evaluate_password(password: str) -> dict:
    checks = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "number": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[^A-Za-z0-9]", password)),
    }

    entropy = calculate_entropy(password)
    pattern_warnings = detect_patterns(password)
    lowered = password.lower()
    in_common_list = lowered in COMMON_PASSWORDS if password else False

    score = 0
    score += 25 if checks["length"] else 0
    score += 15 if len(password) >= 12 else 0
    score += 15 if checks["uppercase"] else 0
    score += 15 if checks["lowercase"] else 0
    score += 15 if checks["number"] else 0
    score += 15 if checks["special"] else 0

    if entropy >= 60:
        score += 10
    elif entropy >= 40:
        score += 5

    if in_common_list:
        score -= 40

    score -= min(len(pattern_warnings) * 10, 25)
    score = max(0, min(score, 100))

    if score >= 85:
        label = "Very Strong"
    elif score >= 70:
        label = "Strong"
    elif score >= 50:
        label = "Moderate"
    elif score >= 30:
        label = "Weak"
    else:
        label = "Very Weak"

    suggestions: list[str] = []
    if not checks["length"]:
        suggestions.append("Use at least 8 characters.")
    if len(password) < 12:
        suggestions.append("Aim for 12+ characters for better resilience.")
    if not checks["uppercase"]:
        suggestions.append("Add an uppercase letter.")
    if not checks["lowercase"]:
        suggestions.append("Add a lowercase letter.")
    if not checks["number"]:
        suggestions.append("Add at least one number.")
    if not checks["special"]:
        suggestions.append("Add a special character.")
    if in_common_list:
        suggestions.append("Avoid commonly used passwords.")
    suggestions.extend(pattern_warnings)

    return {
        "password": password,
        "score": score,
        "label": label,
        "entropy": entropy,
        "checks": checks,
        "common_password": in_common_list,
        "patterns": pattern_warnings,
        "suggestions": suggestions[:6],
    }
