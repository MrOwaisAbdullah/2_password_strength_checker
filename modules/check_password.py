import re

def check_password_strength(password):
    common_passwords = ["password", "123456", "qwerty", "admin", "password123"]
    score = 0
    feedback = []
    is_common = password.lower() in common_passwords
    strength_bar = 0

    if is_common:
        feedback.append("This password is too common and insecure.")
    if len(password) >= 8:
        score += 1
        strength_bar += 25
    else:
        feedback.append("Password should be at least 8 characters long.")
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
        strength_bar += 25
    else:
        feedback.append("Include both uppercase and lowercase letters.")
    if re.search(r"\d", password):
        score += 1
        strength_bar += 25
    else:
        feedback.append("Add at least one number (0-9).")
    if re.search(r"[!@#$%^&*]", password):
        score += 1
        strength_bar += 25
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")

    strength = "Weak" if is_common or score < 3 else "Moderate" if score == 3 else "Strong"
    return strength, feedback, strength_bar