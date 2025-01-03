from cryptography.fernet import Fernet
from os import environ

FERNET_KEY = environ.get("FERNET_KEY")


def fernet_encrypt(value: str) -> str:
    f = Fernet(FERNET_KEY)
    return f.encrypt(value.encode()).decode()


def fernet_decrypt(value: str) -> str:
    f = Fernet(FERNET_KEY)
    return f.decrypt(value).decode()
