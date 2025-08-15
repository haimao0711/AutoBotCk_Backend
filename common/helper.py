import secrets
import hashlib


def generate_random_key(length=32):
    # Generate a random string of alphanumeric characters
    random_string = secrets.token_hex(length)
    return random_string


def hash_api_key(api_key):
    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the API key
    sha256.update(api_key.encode('utf-8'))

    # Get the hashed API key as a hexadecimal string
    hashed_key = sha256.hexdigest()
    return hashed_key


def init_api_key():
    random_key = generate_random_key()
    return hash_api_key((random_key))
