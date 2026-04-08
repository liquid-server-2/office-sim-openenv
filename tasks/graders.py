
def email_grade(action, expected):
    return 1.0 if expected in action.lower() else 0.2

def meeting_grade(action, expected):
    return 1.0 if expected in action.lower() else 0.3

def doc_grade(action, expected):
    return 1.0 if expected in action.lower() else 0.4
