# Authentication Helpers


# Validate passwords
def is_valid_password(password, confirm):
    return password.lower() == confirm.lower() and password.isalnum() and len(password) >= 12
