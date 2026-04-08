def normalize_score(score: float) -> float:
    """
    Ensures score is strictly between (0, 1)
    """
    if score <= 0.0:
        return 0.1
    if score >= 1.0:
        return 0.99
    return score


def email_grade(action: str, expected: str) -> float:
    action = action.lower()

    if expected in action:
        score = 0.9
    elif any(word in action for word in ["urgent", "important"]):
        score = 0.6
    else:
        score = 0.2

    return normalize_score(score)


def meeting_grade(action: str, expected: str) -> float:
    action = action.lower()

    if expected in action:
        score = 0.85
    elif any(word in action for word in ["schedule", "meeting", "time"]):
        score = 0.6
    else:
        score = 0.25

    return normalize_score(score)


def doc_grade(action: str, expected: str) -> float:
    action = action.lower()

    if expected in action:
        score = 0.9
    elif any(word in action for word in ["risk", "issue", "missing"]):
        score = 0.65
    else:
        score = 0.3

    return normalize_score(score)