from cryptography.hazmat.primitives.asymmetric import padding  #  pip install cryptography
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import json
import base64


class Crypto:

    chunk_size = 50  # RSA암호화는 길면 에러남
    private_key = ''
    public_key = ''

    def __init__(self):
        self.private_key = self.load_private_key_from_file('private_key.pem')
        self.public_key = self.load_public_key_from_file('public_key.pem')

    def encrypts(self, message):
        encrypted_message = self.encrypt(message)
        return base64.b64encode(encrypted_message).decode('utf-8')

    def decrypts(self, message):
        decrypted_message = base64.b64decode(message)
        return self.decrypt(decrypted_message)

    def encrypts_long(self, message):
        chunks = [
            message[i:i + self.chunk_size]
            for i in range(0, len(message), self.chunk_size)
        ]
        encrypted_chunks = [self.encrypt(chunk) for chunk in chunks]
        base64_encrypted_chunks = [
            base64.b64encode(chunk).decode('utf-8')
            for chunk in encrypted_chunks
        ]
        return json.dumps(base64_encrypted_chunks)

    def decrypts_long(self, encrypted_chunks):
        base64_encrypted_chunks = json.loads(encrypted_chunks)
        encrypted_chunks = [
            base64.b64decode(chunk) for chunk in base64_encrypted_chunks
        ]
        decrypted_chunks = [self.decrypt(chunk) for chunk in encrypted_chunks]
        return ''.join(decrypted_chunks)

    def encrypt(self, message):
        ciphertext = self.public_key.encrypt(
            message.encode('utf-8'),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None))
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None))
        return plaintext.decode('utf-8')

    def load_private_key_from_file(self, filename):
        with open(filename, 'rb') as f:
            private_key_data = f.read()
            private_key = serialization.load_pem_private_key(
                private_key_data, password=None, backend=default_backend())
        return private_key

    def load_public_key_from_file(self, filename):
        with open(filename, 'rb') as f:
            public_key_data = f.read()
            public_key = serialization.load_pem_public_key(
                public_key_data, backend=default_backend())
        return public_key