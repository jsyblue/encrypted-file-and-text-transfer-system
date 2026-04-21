from cryptography.fernet import Fernet

def generate_symmetric_key():
    return Fernet.generate_key()

def encrypt_symmetric(message: bytes, key: bytes) -> bytes:
    cipher = Fernet(key)
    return cipher.encrypt(message)

def decrypt_symmetric(ciphertext: bytes, key: bytes) -> bytes:
    cipher = Fernet(key)
    return cipher.decrypt(ciphertext)