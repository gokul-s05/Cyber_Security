import string
import secrets

def check_password_strength(password):
    """
    Check password strength and return analysis
    :param password: Password to check
    :return: Tuple of (analysis_text, strength_score)
    """
    strength = 0
    remarks = ''
    lower_count = upper_count = num_count = wspace_count = special_count = 0

    for char in list(password):
        if char in string.ascii_lowercase:
            lower_count += 1
        elif char in string.ascii_uppercase:
            upper_count += 1
        elif char in string.digits:
            num_count += 1
        elif char == ' ':
            wspace_count += 1
        else:
            special_count += 1

    if lower_count >= 1:
        strength += 1
    if upper_count >= 1:
        strength += 1
    if num_count >= 1:
        strength += 1
    if wspace_count >= 1:
        strength += 1
    if special_count >= 1:
        strength += 1

    if strength == 1:
        remarks = ('That\'s a very bad password. Change it as soon as possible.')
    elif strength == 2:
        remarks = ('That\'s a weak password. You should consider using a tougher password.')
    elif strength == 3:
        remarks = 'Your password is okay, but it can be improved.'
    elif strength == 4:
        remarks = ('Your password is hard to guess. But you could make it even more secure.')
    elif strength == 5:
        remarks = ('Now that\'s one hell of a strong password!!! Hackers don\'t have a chance guessing that password!')

    analysis = f'Your password has:\n{lower_count} lowercase letters\n{upper_count} uppercase letters\n{num_count} digits\n{wspace_count} whitespaces\n{special_count} special characters\nPassword Score: {strength}/5\nRemarks: {remarks}'
    return analysis, strength

def generate_password(length=12):
    """
    Generate a random secure password
    :param length: Length of the password
    :return: Generated password
    """
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))

if __name__ == '__main__':
    # Example usage
    test_password = "Hello123!@#"
    analysis, score = check_password_strength(test_password)
    print(f"Testing password: {test_password}")
    print(analysis)
    print(f"\nGenerated password: {generate_password()}")
