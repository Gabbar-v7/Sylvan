import hashlib
import hmac
from os import environ

HASH_KEY = environ.get("HASH_KEY")


def generate_secure_hash(data: str) -> str:
    # Use HMAC with SHA-256 for a secure hash
    hashed_data = hmac.new(HASH_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()
    return hashed_data
