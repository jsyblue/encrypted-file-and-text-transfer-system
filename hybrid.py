def hybrid_encrypt(message: bytes, public_key):
    # Generate AES key
    sym_key = generate_symmetric_key()

    # Encrypt message with AES
    encrypted_message = encrypt_symmetric(message, sym_key)

    # Encrypt AES key with RSA
    encrypted_key = encrypt_rsa(sym_key, public_key)

    return encrypted_key, encrypted_message


def hybrid_decrypt(encrypted_key, encrypted_message, private_key):
    # Decrypt AES key
    sym_key = decrypt_rsa(encrypted_key, private_key)

    # Decrypt message
    return decrypt_symmetric(encrypted_message, sym_key)