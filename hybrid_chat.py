from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import os


def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    with open("private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return private_key, public_key


def load_public_key():
    with open("public.pem", "rb") as f:
        return serialization.load_pem_public_key(f.read())


def load_private_key():
    with open("private.pem", "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def hb_encrypt(message: str):
    aes_key = Fernet.generate_key()
    cipher = Fernet(aes_key)

    encrypted_message = cipher.encrypt(message.encode())

    public_key = load_public_key()

    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_message, encrypted_key


def hb_decryption(encrypted_message, encrypted_key):
    private_key = load_private_key()

    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = Fernet(aes_key)
    return cipher.decrypt(encrypted_message).decode()


if __name__ == "__main__":
    if not os.path.exists("private.pem"):
        generate_rsa_keys()

    msg = input("Enter text > ")

    enc_msg, enc_key = hb_encrypt(msg)

    print("Encrypted:", enc_msg)

    dec = hb_decryption(enc_msg, enc_key)

    print("Decrypted:", dec)