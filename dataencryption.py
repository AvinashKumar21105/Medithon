import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class Encryption():
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        with open('private_key.pem', 'rb') as f:
            pk = serialization.load_pem_private_key(
                f.read(),
                password=b'sachin'
            )
        self.public_key = pk.public_key()
        private_pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(b'sachin')
        )
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open('public_key.pem', 'wb') as f:
            f.write(public_pem)
        with open('private_key.pem', 'wb') as f:
            f.write(private_pem)

    def generate_aes_key(self):
        return os.urandom(32)  # Generate a 256-bit key for AES-256

    def encrypt_data(self,data, aes_key):
        iv = os.urandom(16)  # Initialization vector for AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
        return iv + encrypted_data  # Prepend IV for use in decryption

    def encrypt_aes_key(self,aes_key):
        encrypted_key = self.public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_key















