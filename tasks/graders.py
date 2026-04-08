def normalize_score(score: float) -> float:
    if score <= 0.0:
        return 0.1
    if score >= 1.0:
        return 0.99
    return score


def email_grade(action: str, expected: str) -> float:
    action = action.lower()
    if expected in action:
        return 0.9
    elif "urgent" in action:
        return 0.6
    return 0.2


def meeting_grade(action: str, expected: str) -> float:
    action = action.lower()
    if expected in action:
        return 0.85
    elif "schedule" in action or "meeting" in action:
        return 0.6
    return 0.25


def doc_grade(action: str, expected: str) -> float:
    action = action.lower()
    if expected in action:
        return 0.9
    elif "risk" in action or "missing" in action:
        return 0.65
    return 0.3
