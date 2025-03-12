import secrets
import string

def generate_password(length=8):
    # Define character sets
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    all_characters = letters + digits + symbols

    password = ''.join(secrets.choice(all_characters) for _ in range(length))
    return password

print(generate_password())