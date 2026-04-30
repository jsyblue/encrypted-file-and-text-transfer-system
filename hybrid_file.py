import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def encrypt_file(file_path):
    # Load public key
    with open("public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Generate AES key
    aes_key = AESGCM.generate_key(bit_length=256)

    nonce = os.urandom(12)
    aesgcm = AESGCM(aes_key)

    # Read file
    with open(file_path, "rb") as f:
        plaintext = f.read()

    # Encrypt file
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    # Encrypt AES key with RSA
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Save encrypted file
    with open(file_path + ".enc", "wb") as f:
        f.write(nonce + ciphertext)

    # Save encrypted AES key
    with open(file_path + ".key", "wb") as f:
        f.write(encrypted_key)

    print("Encryption complete")


def decrypt_file(enc_file, key_file):
    # Load private key
    with open("private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # Load encrypted AES key
    with open(key_file, "rb") as f:
        encrypted_key = f.read()

    # Decrypt AES key
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Read encrypted file
    with open(enc_file, "rb") as f:
        data = f.read()

    nonce = data[:12]
    ciphertext = data[12:]

    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    # Restore original filename
    output_file = enc_file.replace(".enc", "")

    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"{output_file} restored successfully")


# Test
encrypt_file("test.txt")
decrypt_file("test.txt.enc", "test.txt.key")