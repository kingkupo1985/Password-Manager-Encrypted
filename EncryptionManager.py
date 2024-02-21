import keyring
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionManager:
    def __init__(self, service_name="password_manager", account_name="user_key"):
        self.service_name = service_name
        self.account_name = account_name
        self.key = self.load_key()

    def generate_key(self):
        # Generate a key
        key = Fernet.generate_key()
        keyring.set_password(self.service_name, self.account_name, key.decode())
        return key

    def load_key(self):
        try:
            key = keyring.get_password(self.service_name, self.account_name)
            if key is None:
                key = self.generate_key()
        except Exception as e:
            print(f"Error loading key: {e}")
            key = self.generate_key()
        return key

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        # Encrypt your data
        cipher = Fernet(self.key)
        encrypted_data = cipher.encrypt(data)
        return encrypted_data

    def decrypt(self, encrypted_data):
        # Decrypt your Data
        cipher = Fernet(self.key)
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        return decrypted_data

    def generate_fernet_key(self, passphrase):
        # Convert passphrase to bytes
        passphrase_bytes = passphrase.encode()

        # Generate a salt (random bytes)
        salt = os.urandom(16)

        # Derive a key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(passphrase_bytes)

        # Create a Fernet key from the derived key
        fernet_key = base64.urlsafe_b64encode(key)
        return fernet_key, salt
