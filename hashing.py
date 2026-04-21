import hashlib

def hash_data(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_hash(data: bytes, hash_value: str) -> bool:
    return hash_data(data) == hash_value