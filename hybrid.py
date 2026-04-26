from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding



class hybrid():
    def generate_rsa_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537 ,
            key_size=2048
        )
        
        public_key = private_key.public_key()

        # save private key
        with open("private.pem","wb")as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
            #save publickey
        with open("private.pem","wb")as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    

    def load_public_key():
        with open("public.pem","rb") as f:
            return serialization.load_pem_public_key(f.read())
        
    
    def load_private_key():
        with open("private.pem","rb") as f:
            return serialization.load_pem_private_key(f.read(),password=None)
        

    #main hybrid code
    #actually important part
    def hb_encrypt (message: str):
        #first generate aes  key
        aes_key = Fernet.generate_key()
        cipher = Fernet(aes_key)

        #2 encrypt message with aes
        encrypted_message = cipher.encrypt(message.encode())

        #3Encrypt AES key with RSA
        public_key = hybrid.load_public_key()
        encrypted_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_message, encrypted_key
    
    def hb_decryption(encrypted_message,encrypted_key):
        #decrypt AES key with RSA
        private_key = hybrid.load_private_key()
        aes_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        #2 decrypt message with aes
        cipher = Fernet(aes_key)
        decrypted_message = cipher.decrypt(encrypted_message)

        return decrypted_message.decode()
    

    #testing

if __name__ == "__main__":
    message = input("enter a text> ")

    encrypted_msg, encrypted_key = hybrid.hb_encrypt(message)

    print("encrypted Message: ", encrypted_msg)
    print("encrypted aes key: ", encrypted_key)

    decrypted_msg = hybrid.hb_decrypt(encrypted_msg, encrypted_key)
    print("decrypt Message: ", decrypted_msg)
