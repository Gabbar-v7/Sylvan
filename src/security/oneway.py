import hashlib
import hmac

from keys import HASH_KEY  # Importing the key from the specified module


def generate_secure_hash(data: str) -> str:
    # Use HMAC with SHA-256 for a secure hash
    hashed_data = hmac.new(HASH_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()
    return hashed_data
