import secrets


def generate_confirmation_token(email):
    random_string = secrets.token_hex(8)
    token = f"{email}-{random_string}"
    return token
